import { format, parseISO } from 'date-fns'
import { ptBR } from 'date-fns/locale'

export const formatDate = (date, formatStr = 'dd/MM/yyyy') => {
  if (!date) return ''
  const parsedDate = typeof date === 'string' ? parseISO(date) : date
  return format(parsedDate, formatStr, { locale: ptBR })
}

export const formatDateTime = (date, formatStr = 'dd/MM/yyyy HH:mm') => {
  if (!date) return ''
  const parsedDate = typeof date === 'string' ? parseISO(date) : date
  return format(parsedDate, formatStr, { locale: ptBR })
}

export const formatTime = (date, formatStr = 'HH:mm') => {
  if (!date) return ''
  const parsedDate = typeof date === 'string' ? parseISO(date) : date
  return format(parsedDate, formatStr, { locale: ptBR })
}
