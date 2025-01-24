---
creator_dcc:
- LINCS
image: /img/playbook_usecase2.png
inputs: phenotype; drug
layout: '@/layouts/UseCase.astro'
link: https://playbook-workflow-builder.cloud/report/c4d40504-57b6-d48f-6d12-d47891e26f2d
short_description: For a side effect and a drug, find differentially expressed genes
  using the LINCS L1000, literature co-mentions, or GWAS. If overlapping genes are
  found, compute whether such overlap is statistically significant and visualize the
  results with a supervenn diagram.
source_dcc:
- LINCS
- KOMP2
sources: GWAS; KOMP; LINCS
title: Explain MOAs of Side Effects for Approved Drugs
tool_icon: https://cfde-drc.s3.us-east-2.amazonaws.com/assets/img/PWB-logo-2024.png
tool_name: Playbook Workflow Builder
tutorial: https://www.youtube.com/watch?v=Y_stZ7wIx_A
---
For a side effect and a drug, find differentially expressed genes from the LINCS L1000 resource that are up- or down-regulated by the drug, and are also associated with the side-effect based on literature co-mentions or GWAS. If overlapping genes are found, compute whether such overlap is statistically significant and visualize the results with a supervenn diagram.