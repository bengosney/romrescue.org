class ModelStatus():
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3

    STATUS_CHOICES = [
        (LIVE_STATUS, 'Published'),
        (HIDDEN_STATUS, 'Unpublished'),
        (DRAFT_STATUS, 'Draft'),
    ]

    @staticmethod
    def getName(status):
        return " ".join([s[1] for s in
                         ModelStatus.STATUS_CHOICES if s[0] == status])
