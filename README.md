<!-- <p align="center" style="display: flex; justify-content: center; gap: 20px;">
  <img src="https://wpimg.wallstcn.com/ecc53a42-d79b-42e2-8852-5126b810a4c8.svg" style="max-width: 100%; height: 100%;">
  <img src="./images/logo.png" style="max-width: 20%; height: 20%;">
</p> -->
<p align="center" style="display: flex; display: flex; align-items: center;">
  <img src="https://wpimg.wallstcn.com/ecc53a42-d79b-42e2-8852-5126b810a4c8.svg">
  <img src="./images/logo.png" style="max-width: 100pt">
</p>


<p align="center">
  <a href="https://github.com/vuejs/vue">
    <img src="https://img.shields.io/badge/vue-2.6.10-brightgreen.svg" alt="vue">
  </a>
  <a href="https://github.com/ElemeFE/element">
    <img src="https://img.shields.io/badge/element--ui-2.7.0-brightgreen.svg" alt="element-ui">
  </a>
  <a href="https://github.com/PanJiaChen/vue-element-admin/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="license">
  </a>
</p>

English | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | [Spanish](./README.es.md)

<!-- <p align="center">
  <b>SPONSORED BY</b>
</p>
<table align="center" cellspacing="0" cellpadding="0">
  <tbody>
    <tr>
      <td align="center" valign="middle">
       <a href="" title="" target="_blank" style="padding-right: 20px;">
        <img height="200px" style="padding-right: 20px;" src="" title="variantForm">
        </a>
      </td>
    </tr>
  </tbody> 
</table>-->

## Introduction

TextileAD-UI is an intuitive tool for training and inference in anomaly detection, designed to help users train and evaluate models without the need for coding. It leverages the [anomalib](https://github.com/open-edge-platform/anomalib) backend for anomaly detection processing and uses [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin) for the frontend user interface.

## Getting started

### System requirements

`Python==3.10`

`npm==6.14.10`

`vue==2.6.10`

#### Browsers support

Modern browsers and Internet Explorer 10+.

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>IE / Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>Chrome | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" alt="Safari" width="24px" height="24px" />](https://godban.github.io/browsers-support-badges/)</br>Safari |
| --------- | --------- | --------- | --------- |
| IE10, IE11, Edge | last 2 versions | last 2 versions | last 2 versions |

### Frontend

```bash
# clone the project
git clone https://github.com/BlueberryOreo/TextileAD-UI.git

# enter the project directory
cd TextileAD-UI

# install dependency
npm install

# develop
npm run dev
```

This will automatically open http://localhost:9527

### Server

```bash
# install dependency
pip install -r requirements.txt

# enter the core directory
cd core

# run
python app.py

# develop
python app.py --debug
```

This will automatically run on http://localhost:5000

## Build

```bash
# build for test environment
npm run build:stage

# build for production environment
npm run build:prod
```

## Advanced

```bash
# preview the release environment effect
npm run preview

# preview the release environment effect + static resource analysis
npm run preview -- --report

# code format check
npm run lint

# code format check and auto fix
npm run lint -- --fix
```

Refer to [Documentation](https://panjiachen.github.io/vue-element-admin-site/guide/essentials/deploy.html) for more information about vue-element-admin

## Snapshots

### Train settings

![train_setting_page1](./images/train_setting_page1.png)

![train_setting_page2](./images/train_setting_page2.png)

### Test settings

![test_setting_page1](./images/test_setting_page1.png)

![test_setting_page2](./images/test_setting_page2.png)

### Training progress

![training_page](./images/training_page.png)

### Results

After training

![results_page_from_train](./images/results_page_from_train.png)

After testing

![results_page_from_test](./images/results_page_from_test.png)

## Acknowledgements

This project is built on [anomalib](https://github.com/open-edge-platform/anomalib) and [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin). The authors thank everyone who makes their code available. 
