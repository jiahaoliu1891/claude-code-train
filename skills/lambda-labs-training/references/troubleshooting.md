# Troubleshooting

## SSH Permission Denied

```
Permission denied (publickey)
```

**Causes:**
1. Wrong SSH key name when launching instance
2. Key permissions too open

**Fixes:**
```bash
# Check key permissions
chmod 600 ~/path/to/key.pem

# Verify key name matches Lambda Labs registration
python scripts/list_instances.py --keys
```

## API 500 Error

**Cause:** Transient server error

**Fix:** Retry after a few seconds. Usually resolves itself.

## No Capacity Available

**Cause:** All GPUs in requested region are in use

**Fixes:**
1. Try different region
2. Try different instance type
3. Wait and retry later
4. Use `--available` flag to see which types have capacity:
   ```bash
   python scripts/list_instances.py --types --available
   ```

## FileSystem Not Mounted

**Cause:** Instance and FileSystem in different regions

**Fix:** Launch instance in same region as FileSystem:
```bash
python scripts/list_instances.py --filesystems  # Check FS region
python scripts/launch_instance.py --type gpu_1x_a100_sxm4 --region us-east-1 ...
```

## Lost Checkpoint After Termination

**Cause:** Checkpoint saved to instance local storage (not FileSystem)

**Prevention:**
1. Create a FileSystem in Lambda Labs dashboard
2. Save outputs to FileSystem path:
   ```bash
   python train.py --out_dir=/home/ubuntu/<filesystem-name>/checkpoints
   ```

## CUDA Out of Memory

**Fixes:**
1. Reduce batch size
2. Enable gradient checkpointing
3. Use mixed precision (bfloat16/float16)
4. Use larger GPU instance
