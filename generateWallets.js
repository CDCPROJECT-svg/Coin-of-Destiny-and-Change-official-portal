
head -n 5 codac_wallets.txt
head -n 5 codac_wallets_thirdweb.csv
wc -l codac_wallets.txthead -n 5 codac_wallets.txt
head -n 5 codac_wallets_thirdweb.csv
wc -l codac_wallets.txt0




const fs = require('fs');
const XLSX = require('xlsx');

// 204-country placeholder (you can expand later)
const countries = Array.from({ length: 204 }, (_, i) => `Country ${i + 1}`);

// Generate PUBLIC ADDRESS ONLY (no keys, no wallet, no ethers)
function generatePublicAddress() {
  const chars = 'abcdef0123456789';
  let address = '0x';
  for (let i = 0; i < 40; i++) {
    address += chars[Math.floor(Math.random() * chars.length)];
  }
  return address;
}

// Build wallets
const wallets = countries.map((country, index) => ({
  Address: generatePublicAddress(),
  Country: country,
  Charity: index < 88 ? 'Yes' : 'No'
}));

// TXT
fs.writeFileSync(
  'codac_wallets.txt',
  wallets.map(w => `${w.Country} | ${w.Address} | Charity: ${w.Charity}`).join('\n')
);

// CSV (metadata)
fs.writeFileSync(
  'codac_wallets.csv',
  ['Address,Country,Charity', ...wallets.map(w => `${w.Address},${w.Country},${w.Charity}`)].join('\n')
);

// CSV (Thirdweb)
fs.writeFileSync(
  'codac_wallets_thirdweb.csv',
  wallets.map(w => w.Address).join('\n')
);

// Excel
const wb = XLSX.utils.book_new();
const ws = XLSX.utils.json_to_sheet(wallets);
XLSX.utils.book_append_sheet(wb, ws, 'CODAC Wallets');
XLSX.writeFile(wb, 'codac_wallets.xlsx');

console.log('✅ CODAC PUBLIC wallet registry generated (NO PRIVATE KEYS)');

