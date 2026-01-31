let currentLevel = 1;

async function updateMotivation() {
    try {
        const response = await fetch('project_roadmap.json');
        const roadmap = await response.json();

        function render(level) {
            const currentData = roadmap.find(p => p.project_id === level);
            const nextData = roadmap.find(p => p.project_id === level + 1);
            const box = document.getElementById('motivation-box');

            if (currentData && box) {
                box.innerHTML = `
                    <div style="background: linear-gradient(135deg, #111, #000); border: 2px solid #D4AF37; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px rgba(212,175,55,0.2);">
                        <h4 style="color: #888; margin: 0; text-transform: uppercase; letter-spacing: 2px;">Current Status</h4>
                        <h2 style="color: #D4AF37; margin: 10px 0;">${currentData.leadership_title}</h2>
                        
                        <div style="background: #222; padding: 15px; border-radius: 10px; margin: 15px 0;">
                            <span style="display:block; color:#888; font-size:12px;">DAILY WITHDRAWAL</span>
                            <span style="font-size: 28px; font-weight: bold; color: #00FF00;">${currentData.daily_withdrawal} USDT</span>
                        </div>

                        <div style="color: #D4AF37; font-size: 14px; margin-bottom: 20px;">
                            Cumulative Potential: <b>${currentData.cumulative_total.toLocaleString()} USDT</b>
                        </div>

                        <p style="font-size: 11px; color: #555;">Next Target: ${nextData ? nextData.leadership_title : 'MAXIMUM RANK REACHED'}</p>
                        
                        <button onclick="alert('Success: ${currentData.daily_withdrawal} USDT processed for current cycle.')" 
                                style="width: 100%; background: #D4AF37; color: black; border: none; padding: 12px; font-weight: bold; border-radius: 5px; cursor: pointer; transition: 0.3s;">
                            WITHDRAW FUNDS
                        </button>
                    </div>
                `;
            }
        }

        render(currentLevel);

        // Auto-demo the progression for the Founder
        const timer = setInterval(() => {
            if (currentLevel < roadmap.length) {
                currentLevel++;
                render(currentLevel);
            } else {
                clearInterval(timer);
            }
        }, 5000);

    } catch (e) { console.error("Roadmap Error:", e); }
}
updateMotivation();
