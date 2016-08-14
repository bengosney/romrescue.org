class ModelStatus():
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3

    STATUS_CHOICES = [
        (LIVE_STATUS, 'Published'),
        (HIDDEN_STATUS, 'Unpublished'),
        (DRAFT_STATUS, 'Draft'),
    ]
