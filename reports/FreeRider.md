## Free rider

### Challenge description

> A new marketplace of Damn Valuable NFTs has been released! There's been an initial mint of 6 NFTs, which are available for sale in the marketplace. Each one at 15 ETH.
>
> A buyer has shared with you a secret alpha: the marketplace is vulnerable and all tokens can be taken. Yet the buyer doesn't know how to do it. So it's offering a payout of 45 ETH for whoever is willing to take the NFTs out and send them their way.
>
> You want to build some rep with this buyer, so you've agreed with the plan.
>
> Sadly you only have 0.5 ETH in balance. If only there was a place where you could get free ETH, at least for an instant. 

### Solution

The FreeRiderNFTMarketplace contract has a vulnerability in `_buyOne()` where `msg.value` is checked and compared to the price of the NFTs which we want to bulk buy through `buyMany()`. However, the comparison is *individually* made for *each* NFT we try to purchase with `buyMany()`. This opens up the possibility of buying *all* NFTs we order for the price of the *highest* one alone, making all others free. 

In this case, we can exploit this by sending 15 ether, which ends up covering for *all* of them (as opposed to 15 * 6 = 90 ether), thereby netting us +75 ether.


