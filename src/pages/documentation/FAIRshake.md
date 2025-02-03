---
layout: '@/layouts/Documentation.astro'
title: FAIR Evaluations with FAIRshake
label: FAIRshake
short_description: The FAIRshake toolkit enables manual and automated assessments of the findability, accessibility, interoperability, and reusability (FAIRness) of digital resources. FAIRshake provides community-driven metrics and rubrics for evaluation, and visualizes the results with a characteristic embeddable insignia. The primary goal of FAIRshake is to enable researchers and developers to objectively measure and improve the FAIRness of their tools.
---
# FAIRshake

## Table of Contents

- [Introduction](#introduction)
- [Resources](#resources)
- [General Steps](#general-steps)
  - [Starting Projects](#starting-projects)
  - [Registering Digital Objects](#registering-digital-objects)
  - [Associating Rubrics](#associating-rubrics)
  - [Performing Assessments](#performing-assessments)

## Introduction

The FAIR data principles -- findability, accessibility, interoperability, and resuability -- were first proposed by <a href="https://www.nature.com/articles/sdata201618" target="_blank">Wilkinson et al. (*Scientific Data*, 2016)</a> to set guidelines for improving data reuse infrastructure in academia. In other words, the FAIR guidelines aim to facilitate continuous reuse of digital objects or re-analysis of data, improve automated knowledge integration, and simplify access to various tools and resources.

Within the CFDE, the FAIR principles are a critical component of our goal to meaningfully synthesize information across Common Fund DCCs to maximize knowledge extraction and promote novel hypothesis generation. To learn more about how DCCs can improve the FAIRness of their digital objects, please see the example code and datasets available in the <a href="https://fairshake.cloud/the-fair-cookbook/intro.html" target="_blank">NIH-CFDE FAIR Cookbook</a>.

## Resources

- <a href="https://fairshake.cloud/" target="_blank">FAIRshake</a>
- <a href="https://fairshake.cloud/static/file/FAIRshakeUserGuide/index.html" target="_blank">FAIRshake User Guide V2</a>
- <a href="https://fairshake.cloud/the-fair-cookbook/intro.html" target="_blank">NIH-CFDE FAIR Cookbook</a>

## General Steps

The steps below are adapted from the <a href="https://fairshake.cloud/static/file/FAIRshakeUserGuide/index.html" target="_blank">FAIRshake User Guide V2</a> and outline the basics of using FAIRshake, including creating a new project, registering digital objects and rubrics within the project, and running a FAIR assessment.

### Starting Projects

1. Navigate to the <a href="https://fairshake.cloud" target="_blank">FAIRshake website</a> and create a user account if you do not already have one.
  ![Sign up for FAIRshake](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image005.jpg?raw=true)

1. Select the **Projects** page from the menu at the top of the page, then click on the **Create New Project** card in the bottom right corner. A project can be used to house a collection of related digital objects that are each associated with at least one FAIR rubric.
  ![Create a new project](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image009.jpg?raw=true)

### Registering Digital Objects

3. Navigate to an existing project or the project you just created, and fill in metadata for a digital object you would like to evaluate. Digital objects may be software, datasets, APIs, or workflows, among others.
  ![Add a Digital Object](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image011.jpg?raw=true)

4. The **Rubrics** field will automatically present a list of potential rubrics that are appropriate for your digital object. If you would like to create your own rubric, see the following section on [Associating Rubrics](#associating-rubrics).
5. Submitting the form will take you to a new page for your now-registered digital object, which displays its metadata and associated projects and rubrics.
  ![View a registered Digital Object](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image013.jpg?raw=true)

### Associating Rubrics

6. To create a new rubric for evaluating your digital object, navigate to the **Rubrics** page via the menu bar, and select the **Create New Rubric** card in the bottom right.
  ![Create a new rubric](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image015.jpg?raw=true)
7. Use the autocomplete **Metrics** field to identify existing metrics, or specific assessment questions, that may be relevant for your rubric. Select as many metrics as you would like; these will be included in your FAIR assessment for the digital objects associated with your rubric.
  ![Auto-complete FAIR metrics](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image017.jpg?raw=true)
    - A pre-existing rubric with list of universal FAIR metrics developed by <a href="https://www.nature.com/articles/sdata201618" target="_blank">Wilkinson et al. (*Scientific Data*, 2016)</a> can be found <a href="https://fairshake.cloud/rubric/25/" target="_blank">here</a>.
      ![FAIR metrics rubric developed by fairmetrics.org](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image019.jpg?raw=true)
1. Submit the form to finish building a rubric. Note that it is not necessary to meticulously cover all FAIR principles in your rubric, as long as they are broadly represented, and the metrics you choose can reasonably determine the FAIRness of your object within the broader community.

### Performing Assessments

9. Ensure that all digital objects in your project have been associated with a rubric.
10. Click on the **Assess** button in the top left corner of a registered digital object's icon, either from the project page or from the digital object page.
11. Select the rubric you would like to use to assess the tool -- it does *not* need to be the auto-selected rubric -- and confirm that the correct digital object and project (if applicable) are also selected.
  ![Selecting a rubric for assessment](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image027.jpg?raw=true)
  ![Assigning the assessment to a project](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image029.jpg?raw=true)
12. Begin the manual assessment of the digital object. For each metric, carefully read and consider the prompts, and then respond to the best of your knowledge. Add any comments or URLS as needed.
  ![Example manual assessment page](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image047.jpg?raw=true)
    - Click on the metric card to the left of any prompt to see more detailed explanations about the metric.
      ![Details about a single metric](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image033.jpg?raw=true)
    - For each metric, you can also examine how other digital objects have scored by clicking the **View Assessments** button from the metric page.
      ![View other assessments associated with a rubric](https://github.com/MaayanLab/FAIRshake/blob/master/FAIRshakeHub/static/file/FAIRshakeUserGuide/files/image035.jpg?raw=true)
13. Once finished, you may save, publish, or delete the assessment.
    - **Publishing** the assessment prevents any further changes, as each digital object in a project can be assessed only once with a given rubric. An insignia and analytics will be generated for the object.
    - **Saving** the assessment means the responses, comments, and URLs will not be public, but will be visible to the creators of the tool, project, and assessment.
    - **Deleting** the assessment will remove all data and responses from the assessment.

#### Return to [Documentation](./)
