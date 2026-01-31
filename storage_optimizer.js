/**
 * CODAC Binary Tree Storage Minimization
 * Strategy:
 * - Projects 2 to 17: Max Depth 25 Levels
 * - Project 18: Cyclical Perfection (L20 -> L21)
 */

const fs = require('fs');
const path = require('path');

function applyProjectLogic() {
    console.log("Applying CODAC Logic: P2-P17 (L25) & P18 (L21)...");

    for (let i = 2; i <= 18; i++) {
        const projectPath = path.join(__dirname, `projects/project_${i}`);
        
        if (!fs.existsSync(projectPath)) {
            fs.mkdirSync(projectPath, { recursive: true });
        }

        let maxDepth, status;

        if (i <= 17) {
            // Logic for Projects 2 to 17
            maxDepth = 25;
            status = "STABLE_L25_LIMIT";
        } else {
            // Logic for Project 18 (The Perfection Cycle)
            maxDepth = 21;
            status = "WAITING_FOR_L20_PERFECTION";
        }

        const config = {
            projectId: i,
            maxDepthLevel: maxDepth,
            currentStatus: status,
            storageMinimization: "ENABLED",
            autoFeedTop: (i === 18), // Only Project 18 triggers the top-feed perfection cycle
            lastUpdate: new Date().toISOString()
        };

        fs.writeFileSync(
            path.join(projectPath, 'logic_config.json'), 
            JSON.stringify(config, null, 2)
        );
        
        console.log(`[Project ${i}] Configuration Set: Max Level ${maxDepth}.`);
    }
    console.log("System Status: Projects 2-17 limited to L25. Project 18 set to L21 Cycle.");
}

applyProjectLogic();
