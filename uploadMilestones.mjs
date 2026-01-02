import { ThirdwebStorage } from "@thirdweb-dev/storage";
import fs from "fs";
import XLSX from "xlsx";

const storage = new ThirdwebStorage();

// Total supply & milestone fees
const totalSupply = 88888888888; // 88,888,888,888
const milestones = [
  { from: 70000000000, to: 50000000000, fee: 0.10 }, // 10%
  { from: 50000000000, to: 40000000000, fee: 0.08 },
  { from: 40000000000, to: 10000000000, fee: 0.04 },
  { from: 10000000000, to: 8888888888, fee: 0.02 },
  { from: 8888888888, to: 0, fee: 0.01 } // fixed
];

// 0.05% split for transfers
const transferSplit = 0.0005;

// Read CSV
const csvFile = fs.readFileSync("cdc_wallets.csv", "utf-8");
const lines = csvFile.trim().split("\n");
const header = lines.shift(); // remove header

async function main() {
  const output = [];

  for (let i = 0; i < lines.length; i++) {
    const [address, country, charity] = lines[i].split(",");

    // Determine milestone allocation
import { ThirdwebStorage } from "@thirdweb-dev/storage";
import fs from "fs";
import XLSX from "xlsx";

const storage = new ThirdwebStorage();

// Total supply & milestone fees
const totalSupply = 88888888888; // 88,888,888,888
const milestones = [
  { from: 70000000000, to: 50000000000, fee: 0.10 }, // 10%
  { from: 50000000000, to: 40000000000, fee: 0.08 },
  { from: 40000000000, to: 10000000000, fee: 0.04 },
  { from: 10000000000, to: 8888888888, fee: 0.02 },
  { from: 8888888888, to: 0, fee: 0.01 } // fixed
];

// 0.05% split for transfers
const transferSplit = 0.0005;

// Read CSV
const csvFile = fs.readFileSync("cdc_wallets.csv", "utf-8");
const lines = csvFile.trim().split("\n");
const header = lines.shift(); // remove header

async function main() {
  const output = [];

  for (let i = 0; i < lines.length; i++) {
    const [address, country, charity] = lines[i].split(",");

    // Determine milestone allocation
    let allocation = 0;

    for (const m of milestones) {
      if (totalSupply <= m.from && totalSupply > m.to) {
        allocation = Math.floor((totalSupply * m.fee) / lines.length);
        break;
      }
    }

    // 0.05% transfer split to groups
    const groupSplit = Math.floor(allocation * transferSplit / 3); // divided into 3 groups

    const metadata = {
      address,
      country,
      charity,
      milestone_allocation: allocation,
      group_split_204: groupSplit,
      group_split_88: groupSplit,
      group_split_tokenomics: groupSplit
    };

    // Upload metadata to Thirdweb IPFS
    const uri = await storage.upload(metadata);

    console.log(`${address} => ${uri}`);
    output.push([address, country, charity, allocation, groupSplit, groupSplit, groupSplit, uri]);
  }

  // Save CSV
  const outCsv = [
    "Address,Country,Charity,MilestoneAllocation,Split_204,Split_88,Split_Tokenomics,IPFS_URI",
    ...output.map(r => r.join(","))
  ].join("\n");
  fs.writeFileSync("cdc_wallets_ipfs.csv", outCsv);

  // Save Excel
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(output);
  XLSX.utils.book_append_sheet(wb, ws, "CDC Wallets");
  XLSX.writeFile(wb, "cdc_wallets_ipfs.xlsx");

  console.log("✅ Wallet metadata + milestone allocations uploaded to IPFS!");
}

main();    let allocation = 0;
    for (const m of milestones) {
      if (totalSupply <= m.from && totalSupply > m.to) {
        allocation = Math.floor((totalSupply * m.fee) / lines.length);
        break;
      }
    }

    // 0.05% transfer split to groups
    const groupSplit = Math.floor(allocation * transferSplit / 3); // divided into 3 groups

    const metadata = {
      address,
      country,
      charity,
      milestone_allocation: allocation,
      group_split_204: groupSplit,
      group_split_88: groupSplit,
      group_split_tokenomics: groupSplit
    };

    // Upload metadata to Thirdweb IPFS
    const uri = await storage.upload(metadata);

    console.log(`${address} => ${uri}`);
    output.push([address, country, charity, allocation, groupSplit, groupSplit, groupSplit, uri]);
  }

  // Save CSV
  const outCsv = [
    "Address,Country,Charity,MilestoneAllocation,Split_204,Split_88,Split_Tokenomics,IPFS_URI",
    ...output.map(r => r.join(","))
  ].join("\n");
  fs.writeFileSync("cdc_wallets_ipfs.csv", outCsv);

  // Save Excel
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(output);
  XLSX.utils.book_append_sheet(wb, ws, "CDC Wallets");
  XLSX.writeFile(wb, "cdc_wallets_ipfs.xlsx");

  console.log("✅ Wallet metadata + milestone allocations uploaded to IPFS!");
}

main();
