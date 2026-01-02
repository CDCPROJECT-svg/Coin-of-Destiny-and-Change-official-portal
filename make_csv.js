const fs = require("fs");

const input = fs.readFileSync("cdc_wallets.txt", "utf8").trim().split("\n");

let csv = "Country,WalletAddress,PrivateKey\n";

for (const line of input) {
  // Expected format:
  // CountryName - Address: 0x123... - PrivateKey: abc...
  const parts = line.split(" - ");

  const country = parts[0];
  const address = parts[1].replace("Address: ", "");
  const privateKey = parts[2].replace("PrivateKey: ", "");

  csv += `"${country}","${address}","${privateKey}"\n`;
}

fs.writeFileSync("cdc_wallets.csv", csv);
console.log("CSV file created: cdc_wallets.csv")

