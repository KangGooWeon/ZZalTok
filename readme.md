# :calendar: 프로젝트 개요

- **진행기간** : 2021.02.24 ~ 2021.04.06
- **목표**
  - 사용자가 원하는 얼굴 사진을 합성
  - 원하는 사진으로 재미난 영상 제작
  - 동영상 배경 제거 및 배경 사진 합성
  - 다양한 합성 결과물들의 게시판 공유와 카카오톡 공유
- **웹사이트 이름** : ZZalTok(짤톡)
  - 사용자의 사진과 동영상을 활용하여 재미를 제공하고 서로 공유하는 서비스

# :wave: 팀원소개

![team](https://user-images.githubusercontent.com/57394523/115139785-e3956e80-a06e-11eb-8b48-3593dcd7580d.PNG)


## :cd: 설치방법

Jenkins 파이프라인을 위한 스크립트를 사용합니다. 해당 문서를 확인해주세요.

### Windows

> #### 서버
>
> 1. [미니콘다](https://docs.conda.io/en/latest/miniconda.html) 설치
> 2. [CUDA 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-base) 설치
> 3. .\back\install.bat 실행
> 4. .\back\run.bat 실행

> #### 클라이언트(Vue.js)
>
> ```cmd
> cd .\front
> npm install
> npm build
> ```

### Linux

`***required docker, jenkins***`

- Defining a [Pipeline in SCM](https://www.jenkins.io/doc/book/pipeline/getting-started#defining-a-pipeline-in-scm),
  a Jenkinsfile is a text file that contains the definition of a Jenkins Pipeline and is checked into source control. Using `Jenkinsfile`.

## :mag: 기능소개

### 얼굴 체인지
![2](https://user-images.githubusercontent.com/57394523/115139802-f60fa800-a06e-11eb-81b4-f239c227f710.gif)

### 다메다메 영상 만들기
![3](https://user-images.githubusercontent.com/57394523/115139800-f4de7b00-a06e-11eb-9d64-d5888aa3de11.gif)

### 동영상 배경 변경하기
![4](https://user-images.githubusercontent.com/57394523/115139804-f740d500-a06e-11eb-8414-669652482e14.gif)

### 짤 공유 기능
![5](https://user-images.githubusercontent.com/57394523/115139838-2fe0ae80-a06f-11eb-8d9c-c13ea2e7ab4c.gif)

### 게시글 기능
![6](https://user-images.githubusercontent.com/57394523/115139839-31aa7200-a06f-11eb-8af5-d6dd26cdb6a5.gif)





## :loudspeaker: 기여

Pull & Merge Request 요청을 환영합니다.

주요 변경 사항은 먼저 문제를 열어 변경하고자 하는 사항에 대해 논의하십시오.

(필요에 따라 테스트를 업데이트하십시오.)

## License

[MIT](https://choosealicense.com/licenses/mit/)
