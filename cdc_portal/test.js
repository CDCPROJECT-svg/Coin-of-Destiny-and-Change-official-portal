import { createThirdwebClient, getContract } from "thirdweb";
import { ethereum } from "thirdweb/chains";

// No erc721 import

const client = createThirdwebClient({
  clientId: "beaa354db6df0c8e91ee38dc3711f377",
});

async function main() {
  const contract = await getContract({
    client,
    address: "0xDF98ba599B20e76D69E8391e6b53C8679F7A3c7b",
    chain: ethereum,
  });

  // Try to access contract metadata using the contract object directly
  const metadata = await contract.metadata.get();
  console.log("Contract metadata:", metadata);
}

main().catch(console.error);
