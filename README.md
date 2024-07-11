
# DeepScale
This repo contains example models that use [DeepScale](https://github.com/khulnasoft/DeepScale).

# Note on Megatron examples

Megatron-LM : This is a fairly old snapshot of Megatron-LM , and we have been using it show case the earlier features of DeepScale. This does not contain ZeRO-3 or 3D parallelism.

Megatron-LM-v1.1.5-3D_parallelism: This is a relatively new Megatron (Oct 2020), but before Megatron started supporting 3D parallelism. We ported this version to showcase how to use 3D parallelism inside DeepScale with Megatron.

Megatron-LM-v1.1.5-ZeRO3: The underlying Megatron version is same as the 3D_parallelism but it does not contain the 3D parallelism port. It however contains the most recent advances in DeepScale including ZeRO-3, ZeRO-3 Offload and ZeRO-Infinity. We did this separately from 3D parallelism port to isolate the changes required for each of them and to avoid users combining them together which is not supported, and will likely lead to more confusion.

Since the 3D parallelism is quite similar in both DeepScale and new Megatron, we don't have plans to update to new version immediately. But we do plan to update it in future as Megatron-LM adds more differentiating features.

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.khulnasoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.khulnasoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.khulnasoft.com/codeofconduct/faq/) or
contact [opencode@khulnasoft.com](mailto:opencode@khulnasoft.com) with any additional questions or comments.
