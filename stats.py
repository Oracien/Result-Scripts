

ADD_PRED = [
"simpleStridesDetected",
"complexStridesDetected",
"operandSimpleStridesDetected",
"operandComplexStridesDetected",
"entriesInserted",
"entriesDeleted",
"failedPredictions",
"confidenceLimitedPredictions",
"pageLimitedPredictions",
"largeStrideLimitedPredictions",
"successfulPredictions"
]

PRED_UNIT = [
"loadsInserted",
"completedLoads",
"loadsCleared",
"predictionsMade",
"predictionsIssued",
"predictionsCleared",
"issuedLoadsInserted",
"issuedLoadsCleared",
"storeForwards",
"partialStoreForwards",
"prunedReadyInsts",
"prunedNonSpecInsts"
]

LSQ_UNIT = [
"forwLoads",
"squashedLoads",
"ignoredResponses",
"memOrderViolation",
"squashedStores",
"rescheduledLoads",
"blockedByCache",
"issuedPredictions",
"blockedPredictions",
"delayedTranslationPredictions",
"committedCorrectPredictions",
"committedIncorrectPredictions",
"storeMemoryVariance",
"wrongDataPredictions",
"sttLoadBypasses",
"L1CacheRuns",
"deepCacheRuns"
]

LSQ_UNIT_DISTRIB = [
"loadToUse",
"loadDecodeToComplete",
"loadDecodeToAddress",
"loadLatencyCorrect",
"loadLatencyIncorrect"
]

LSQ_UNIT_DISTRIB_INT = [
(0, 299, 10),
(0, 299, 5),
(0, 299, 5),
(0, 299, 5),
(0, 299, 5)
]

DISTRIB_CONST = [
"samples",
"mean",
"stdev",
"overflows",
"min_value",
"max_value",
"total"
]


def get_stats(stat_groups):
    stats = []
    for x in stat_groups:
        stats.extend(x)
    return stats

def generate_distrib():
    assert(len(LSQ_UNIT_DISTRIB) == len(LSQ_UNIT_DISTRIB_INT))
    stats = []
    for i in range(len(LSQ_UNIT_DISTRIB)):
        name = LSQ_UNIT_DISTRIB[i]
        for stat in DISTRIB_CONST:
            stats.append(f"lsq0.{name}::{stat}")
        intervals = LSQ_UNIT_DISTRIB_INT[i]
        for j in range(intervals[0], intervals[1], intervals[2]):
            stats.append(f"lsq0.{name}::{j}-{j+intervals[2]-1}")

LSQ_UNIT_GEN_STATS = generate_distrib()

