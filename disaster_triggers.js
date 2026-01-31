// STRICT COMPUTATION LOGIC - DO NOT ALTER
// Rule: Withdrawal matches population impact % exactly.
// Split: 28.88% Liquid, 71.12% Reserve.

function calculateDisasterRelief(totalCountryFund, affectedPopPercent) {
    // Exact percentage withdrawal
    let totalWithdrawn = totalCountryFund * (affectedPopPercent / 100);

    // Strict split of the withdrawn amount
    let liquidRelief_2888 = totalWithdrawn * 0.2888;
    let reliefReserve_7112 = totalWithdrawn * 0.7112;

    return {
        totalWithdrawn: totalWithdrawn.toFixed(4),
        liquidRelief: liquidRelief_2888.toFixed(4),
        reserveRelief: reliefReserve_7112.toFixed(4)
    };
}

console.log("Disaster Logic Locked: Withdrawal = Pop %, Split = 28.88/71.12");
