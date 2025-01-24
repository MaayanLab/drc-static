---
creator_dcc:
- LINCS
image: /img/playbook_usecase1.png
inputs: phenotype; drug; drug
layout: '@/layouts/UseCase.astro'
link: https://playbook-workflow-builder.cloud/report/6a7af61b-ef0a-7687-5d6e-02deeb253172
short_description: For an adverse event known to be caused by drug-drug interactions,
  I would like to know if there are overlapping genes between genes that are up or
  down regulated by the drugs from LINCS and genes associated with the adverse event
  based on GWAS, literature co-mentions, and genes associated with mouse and human
  phenotypes.
source_dcc:
- LINCS
- KOMP2
sources: KOMP; HPO; GWAS; Geneshot; LINCS
title: Explain Drug-Drug Interactions
tool_icon: https://cfde-drc.s3.us-east-2.amazonaws.com/assets/img/PWB-logo-2024.png
tool_name: Playbook Workflow Builder
tutorial: https://www.youtube.com/watch?v=7_Xir0jVisM
---
Give two drugs and an adverse event that is known to be caused by the drug-drug interactions, I would like to know if there are overlapping genes between genes that are either up or down regulated by the drugs from LINCS and genes associated with the adverse event either based on GWAS, gene mentions in the literature, and genes associated with mouse and human phenotypes. I would like to also know if the overlap between these genes is statistically significant. I would also like to have the results visualized as a Venn diagram.