class MessageStatus:
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"

    VALID_STATUSES = {
        SENT,
        DELIVERED,
        READ,
    }