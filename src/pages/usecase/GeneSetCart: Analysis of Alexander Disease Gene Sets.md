---
creator_dcc:
- LINCS
image: /img/g2sg_axd.png
inputs: gene sets
layout: '@/layouts/UseCase.astro'
link: https://genesetcart.cfde.cloud/use-cases
short_description: Alexander disease (AxD) is caused by a GFAP gene mutation, leading
  to an accumulation of GFAP protein. This excess GFAP leads to Rosenthal fibers (RFs)
  in astrocytes. We use the G2SG pipeline to analyze gene sets created by comparing
  gene expression samples obtained from GEO of wild type (WT) or controls to Alexander
  disease samples.
source_dcc:
- LINCS
sources: GEO; Appyters; SigCom LINCS;
title: Analysis of Alexander Disease Gene Sets
tool_icon: https://cfde-drc.s3.us-east-2.amazonaws.com/assets/img/g2sg-logo.png
tool_name: GeneSetCart
---
Alexander disease (AxD) is a rare neurodegenerative disease caused by a mutation in the GFAP gene that codes for the glial fibrillary acidic protein (GFAP)[1]. GFAP protein supports the brain's white matter (the myelin sheath) at normal levels but in Alexander disease, the gain-of-function mutation of the GFAP gene causes this protein to accumulate. Instead of helping maintain myelin, the extra GFAP kills other cells and damages the myelin. The overexpression of GFAP also results in the appearance and growth of Rosenthal fibers (RFs) which are protein aggregates in the cytoplasm of astrocytes [2]. The Gene Expression Omnibus (GEO) is a major open biomedical research repository for transcriptomics and other omics datasets that currently contains millions of gene expression samples from tens of thousands of studies collected by research laboratories [3]. Here, we use the G2SG pipeline to analyze gene sets created by comparing gene expression samples obtained from GEO of wild type (WT) or controls to alexander disease samples.