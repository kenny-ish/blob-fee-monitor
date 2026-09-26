# blob-fee-monitor

Shows the state of the EIP-4844 blob fee market on Ethereum. Rollups post their data as blobs, which
have their own base fee, separate from normal gas.

```bash
python blobs.py
python blobs.py --blocks 100 --watch 60
```

It uses two fields of `eth_feeHistory(N, "latest", [])`:

- `baseFeePerBlobGas`, the blob base fee of each block. The last entry is for the next block.
- `blobGasUsedRatio`, how full each block's blob space was compared with the maximum.

The output has the next blob base fee, its minimum, average and maximum over the window, the average
utilization, the cost of one blob (131,072 blob gas) in ETH and a small trend chart. The blob base
fee rises when blocks are above the blob target and falls when they are below, so utilization that
stays above the target means fees are going up.

It works on any chain whose `eth_feeHistory` returns the blob fields. If they're missing, the tool
reports that the chain has no blob data.

## Tests

```bash
python -m unittest -v
```
