# PATH: src/core/domain/events/__init__.py
# DESC: Domain events module: __init__.py.

from src.core.domain.events.base import DomainEvent
from src.core.domain.events.analysis_events import (
    AnalysisCompleted,
    AnalysisFailed,
    AnalysisRequested,
    AnalysisStarted,
    CalibrationValidated,
    LowConfidenceDetected,
)
from src.core.domain.events.expert_events import (
    ExpertActivated,
    ExpertDeactivated,
    ExpertRegistered,
    FeedbackProvided,
)
from src.core.domain.events.expert_review_events import (
    ExpertReviewAssigned,
    ExpertReviewCompleted,
    ExpertReviewEscalated,
    ExpertReviewRequested,
)
from src.core.domain.events.field_events import (
    FieldCreated,
    FieldCropUpdated,
    FieldDeleted,
    FieldUpdated,
)
from src.core.domain.events.mission_events import (
    DataUploaded,
    MissionAnalysisRequested,
    MissionAssigned,
    MissionCancelled,
    MissionCompleted,
    MissionReplanQueued,
    MissionStarted,
)
from src.core.domain.events.payment_events import (
    PaymentApproved,
    PaymentIntentCreated,
    PaymentRejected,
    ReceiptUploaded,
)
from src.core.domain.events.subscription_events import (
    MissionScheduled,
    SubscriptionActivated,
    SubscriptionCompleted,
    SubscriptionCreated,
    SubscriptionRescheduled,
)
from src.core.domain.events.training_feedback_events import (
    TrainingDataExported,
    TrainingFeedbackAccepted,
    TrainingFeedbackRejected,
    TrainingFeedbackSubmitted,
)

__all__: list[str] = [
    # Base
    "DomainEvent",
    # Analysis (KR-017, KR-018)
    "AnalysisRequested",
    "AnalysisStarted",
    "AnalysisCompleted",
    "AnalysisFailed",
    "CalibrationValidated",
    "LowConfidenceDetected",
    # Expert (KR-019)
    "ExpertRegistered",
    "ExpertActivated",
    "ExpertDeactivated",
    "FeedbackProvided",
    # Expert Review (KR-019)
    "ExpertReviewRequested",
    "ExpertReviewAssigned",
    "ExpertReviewCompleted",
    "ExpertReviewEscalated",
    # Field
    "FieldCreated",
    "FieldUpdated",
    "FieldCropUpdated",
    "FieldDeleted",
    # Mission (KR-015)
    "MissionAssigned",
    "MissionStarted",
    "DataUploaded",
    "MissionAnalysisRequested",
    "MissionCompleted",
    "MissionCancelled",
    "MissionReplanQueued",
    # Payment (KR-033)
    "PaymentIntentCreated",
    "ReceiptUploaded",
    "PaymentApproved",
    "PaymentRejected",
    # Subscription (KR-015-5)
    "SubscriptionCreated",
    "SubscriptionActivated",
    "MissionScheduled",
    "SubscriptionCompleted",
    "SubscriptionRescheduled",
    # Training Feedback (KR-019)
    "TrainingFeedbackSubmitted",
    "TrainingFeedbackAccepted",
    "TrainingFeedbackRejected",
    "TrainingDataExported",
]
