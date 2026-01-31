const SYSTEM_MAINTENANCE_LOCK = true; 

const CODAC_CONFIG = {
    PROJECTS_COUNT: 18,
    MAIN_PROJECT_MAX: 28,
    SUB_PROJECT_MAX: 20,
    GUARDIAN_LEVEL: 7,
    MERCHANT_COMMISSION: 0.08,
    REWARD_DIVIDER: 8
};

// Enforces the 28-level feeding and 20-level project limits
function checkLevelCap(projectId, currentLevel) {
    if (SYSTEM_MAINTENANCE_LOCK) return "LOCKED";
    const limit = (projectId === 1) ? CODAC_CONFIG.MAIN_PROJECT_MAX : CODAC_CONFIG.SUB_PROJECT_MAX;
    return currentLevel >= limit;
}

// Calculates 8% commission and the "Divide by 8" rewards
function calculateMerchantPoints(grossSale) {
    if (SYSTEM_MAINTENANCE_LOCK) return "LOCKED";
    const commission = grossSale * CODAC_CONFIG.MERCHANT_COMMISSION;
    const userReward = commission / CODAC_CONFIG.REWARD_DIVIDER;
    return {
        merchantFee: commission,
        userPoints: userReward
    };
}

console.log("CODAC Core Logic: 18 Projects Locked & Secured for Maintenance.");

