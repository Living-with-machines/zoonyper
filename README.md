# About `zoonyper`

[![All Contributors](https://img.shields.io/github/all-contributors/Living-with-machines/zoonyper?color=ee8449&style=flat-square)](#contributors)

**Zoonyper** is a Python library, designed to make it easy for users to import and process Zooniverse annotations and their metadata in your own Python code. It is especially designed for use in [Jupyter Notebooks](https://jupyter.org/).

## Purpose
The [Zooniverse citizen science platform's Project Builder](https://www.zooniverse.org/lab) allows anyone to create crowdsourced tasks using uploaded or [imported images](https://blogs.bl.uk/digital-scholarship/2022/04/importing-images-into-zooniverse-with-a-iiif-manifest-introducing-an-experimental-feature.html) and other media. However, its flexibility means that the data created can be difficult to process.

Zoonyper can help process the output files from the Zooniverse citizen science platform, and facilitate data wrangling, compression, and output into JSON and CSV files. The output files can then be more easily used in e.g. Observable visualisations, Excel and other tools.

## Background

The library was created as part of the [Living with Machines project](https://livingwithmachines.ac.uk), a research project developing historical and data science methods to study the effects of the mechanisation on the lives of ordinary people during the long nineteenth century. 

As part of that work, we used digitised historical newspapers at scale. We chose crowdsourcing as a method for some of this work so that we could invite the public to actively contribute to our research, observe how training data is created and annotated for machine learning, and to view the source material we were using across the project. We used the Zooniverse project builder as it is designed for citizen science projects where volunteers contribute to scientific research projects by annotating and categorizing images or other data. The annotations created by volunteers are collected as "classifications" in the Zooniverse system.

We queried digitised newspapers for keywords related to our research topics, uploaded the images, automatically transcribed text (OCR) and metadata about the selected articles to Zooniverse, then asked volunteers to help us with classifications or transcriptions (typing in text) of those articles. The final goal for the research overall was to use the annotations to study the content of these historical newspapers and gain insights into the events and trends of the past.

## Getting started

Here's how you can use Zoonyper in your own project:

1. **Install the repository**: First, you'll need to install the repository. You can do this by cloning the repository or installing it using [the instructions below](#installation).

2. **Import the `Project` class**: Once you've installed the repository, you can import the `Project` class into your own Python code. You can do this by adding the following line to the top of your code:

   ```py
   from zoonyper import Project
   ```

3. **Initialize a `Project` object**: To start using the Project class, you'll need to create a Project object. You can do this by calling the constructor and passing in the path to the directory that contains all the files from your Zooniverse project lab\*:

   ```py
   project = Project("<path to the directory with all necessary files>")
   ```

4. **Access the project's data and metadata**: Once you have a `Project` object, you can access its annotations by using the `.classifications` attribute. This attribute is a Pandas DataFrame, where each row contains information about a single classification, including annotations.

5. **Process the data and metadata**: Because the data structures in Zoonyper are Pandas DataFrames, you can process the classifications, subjects, and annotations in any way you like, using the tools and techniques that you're familiar with. For example, you might want to calculate statistics about the annotations, or create plots to visualize the data.

## Preparing your Zooniverse files

Via Zooniverse's web 'Lab' interface, go to the Data Exports page. Request and download these exports:

- classification export
- subject export
- workflow export
- talk comments

They should be named "classifications.csv", "subjects.csv", "workflows.csv", and "comments.json" and "tags.json" respectively, placed in a folder. This folder's path is what should be passed to the `Project` constructor.

## Installation

<!--
Installing through `pip`:

```sh
$ pip install zoonyper
```
-->

Because this project is in **active development**, you need to install from the repository for the time being. In order to do so, follow [the installation instructions](docs/source/installing.rst).

## Documentation

You can see the public documentation on https://living-with-machines.github.io/zoonyper.

You can contribute to the documentation using [`sphinx`](https://www.sphinx-doc.org/en/master/) to edit and render the [`docs`](docs) directory.

## Data model

The Zoonyper dataframes' data model is illustrated in the following diagram.

```mermaid
erDiagram
    workflow ||--|{ annotation : has
    workflow }|--o{ subject_set: has
    subject_set }|--|{ subject: contains
    annotation ||--|| subject: on
    user ||..|{ annotation : makes
    user ||..|{ comment : writes
    tag }|--|{ comment : in
    comment ||--o{ subject : "written about"
```

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://www.westerling.nu"><img src="https://avatars.githubusercontent.com/u/7298727?v=4?s=100" width="100px;" alt="Kalle Westerling"/><br /><sub><b>Kalle Westerling</b></sub></a><br /><a href="https://github.com/Living-with-machines/zoonyper/commits?author=kallewesterling" title="Documentation">📖</a> <a href="#ideas-kallewesterling" title="Ideas, Planning, & Feedback">🤔</a> <a href="#projectManagement-kallewesterling" title="Project Management">📆</a> <a href="https://github.com/Living-with-machines/zoonyper/pulls?q=is%3Apr+reviewed-by%3Akallewesterling" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://openobjects.org.uk"><img src="https://avatars.githubusercontent.com/u/380763?v=4?s=100" width="100px;" alt="Mia"/><br /><sub><b>Mia</b></sub></a><br /><a href="https://github.com/Living-with-machines/zoonyper/commits?author=mialondon" title="Documentation">📖</a> <a href="#ideas-mialondon" title="Ideas, Planning, & Feedback">🤔</a> <a href="#projectManagement-mialondon" title="Project Management">📆</a> <a href="https://github.com/Living-with-machines/zoonyper/pulls?q=is%3Apr+reviewed-by%3Amialondon" title="Reviewed Pull Requests">👀</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jmiguelv"><img src="https://avatars.githubusercontent.com/u/1233186?v=4?s=100" width="100px;" alt="Miguel Vieira"/><br /><sub><b>Miguel Vieira</b></sub></a><br /><a href="https://github.com/Living-with-machines/zoonyper/commits?author=jmiguelv" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
