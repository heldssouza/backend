from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

# Database metrics
DB_CONNECTION_COUNT = Gauge(
    'database_connections',
    'Number of active database connections',
    ['database']
)

DB_QUERY_COUNT = Counter(
    'database_queries_total',
    'Total number of database queries',
    ['operation', 'table']
)

DB_QUERY_DURATION = Histogram(
    'database_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

# Business metrics
TENANT_COUNT = Gauge(
    'tenant_count',
    'Number of active tenants'
)

USER_COUNT = Gauge(
    'user_count',
    'Number of active users',
    ['tenant']
)

TRANSACTION_COUNT = Counter(
    'transaction_count',
    'Number of financial transactions',
    ['tenant', 'type']
)

# System metrics
MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage'
)


class MetricsMiddleware:
    """Middleware to collect request metrics"""
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        start_time = time.time()
        
        # Get request details
        method = scope["method"]
        path = scope["path"]
        
        # Process request
        response = await self.app(scope, receive, send)
        
        # Record metrics
        duration = time.time() - start_time
        status = response.status_code
        
        REQUEST_COUNT.labels(
            method=method,
            endpoint=path,
            status=status
        ).inc()
        
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=path
        ).observe(duration)
        
        return response


class DatabaseMetrics:
    """Context manager to collect database metrics"""
    
    def __init__(self, operation: str, table: str):
        self.operation = operation
        self.table = table
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        DB_QUERY_COUNT.labels(
            operation=self.operation,
            table=self.table
        ).inc()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        DB_QUERY_DURATION.labels(
            operation=self.operation,
            table=self.table
        ).observe(duration)


def update_business_metrics(db_session):
    """Update business metrics"""
    from app.models.master.tenant import Tenant
    from app.models.master.user import User
    
    # Update tenant count
    tenant_count = db_session.query(Tenant).filter(
        Tenant.is_active == True
    ).count()
    TENANT_COUNT.set(tenant_count)
    
    # Update user count per tenant
    tenants = db_session.query(Tenant).filter(
        Tenant.is_active == True
    ).all()
    
    for tenant in tenants:
        user_count = db_session.query(User).filter(
            User.tenant_id == tenant.tenant_id,
            User.is_active == True
        ).count()
        USER_COUNT.labels(tenant=tenant.name).set(user_count)


def update_system_metrics():
    """Update system metrics"""
    import psutil
    
    # Memory usage
    memory = psutil.virtual_memory()
    MEMORY_USAGE.set(memory.used)
    
    # CPU usage
    CPU_USAGE.set(psutil.cpu_percent())
