const fs = require("fs");
const XLSX = require("xlsx");

// Read your wallets
const input = fs.readFileSync("codac_wallets.txt", "utf8").trim().split("\n");

// Prepare array for Excel rows
let data = [];
let country = "";
let address = "";
let privateKey = "";

for (const line of input) {
  if (line.startsWith("Country: ")) {
    country = line.replace("Country: ", "").trim();
  } else if (line.startsWith("Address: ")) {
    address = line.replace("Address: ", "").trim();
  } else if (line.startsWith("Private Key: ")) {
    privateKey = line.replace("Private Key: ", "").trim();
    data.push({ Country: country, WalletAddress: address, PrivateKey: privateKey });
    country = "";
    address = "";
    privateKey = "";
  }
}

// Create a new workbook
const wb = XLSX.utils.book_new();
const ws = XLSX.utils.json_to_sheet(data);

// Append worksheet
XLSX.utils.book_append_sheet(wb, ws, "CODAC Wallets");

// Write to Excel file
XLSX.writeFile(wb, "codac_wallets.xlsx");

console.log("✅ Excel file created: codac_wallets.xlsx");
