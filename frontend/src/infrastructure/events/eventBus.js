import mitt from 'mitt'

const eventBus = mitt()

export const EventTypes = {
  TENANT_CHANGED: 'TENANT_CHANGED',
  USER_UPDATED: 'USER_UPDATED',
  LANGUAGE_CHANGED: 'LANGUAGE_CHANGED',
  SESSION_EXPIRED: 'SESSION_EXPIRED',
  NOTIFICATION: 'NOTIFICATION'
}

export default eventBus
