<template>
  <v-app>
    <div>
      <div><v-img src="@/assets/banner1.png" alt="" max-width="100%" max-height="300px" /></div>
      <div>
        <v-container>
          <div :class="{ hide: isHide }">
            <v-row no-gutters justify="center" style="margin-right: 50px; margin-left: 50px">
              <v-col cols="3"></v-col>

              <v-col>
                <v-row no-gutters justify="center" ref="printMe">
                  <v-col> <img :src="previewImgUrl" alt="" style="width: 100%; height: 100%" /> </v-col>
                  <v-col class="font-change" style="background: black; text-align: center">
                    <div style="color: white"><p v-html="OutProverbContent"></p></div>
                    <div style="color: white"><p v-html="OutProverbName"></p></div>
                  </v-col>
                </v-row>
              </v-col>

              <v-col cols="3"></v-col>
            </v-row>
          </div>

          <FileUpload type="image" v-on:fileUpload="originUpload" v-on:removeImg="removeOriginImg" content="배경 사진"></FileUpload>
          <FileUpload type="image" v-on:fileUpload="targetUpload" v-on:removeImg="removeTargetImg" content="합성 할 사진"></FileUpload>

          <v-container>
            <v-row no-gutters justify="center">
              <v-col></v-col>
              <v-col>
                명언
                <textarea
                  label="명언입력"
                  hide-details="auto"
                  v-model="proverb.proverbContent"
                  style="resize: none; width: 100%; border: 1px solid black"
                ></textarea>
              </v-col>

              <v-col></v-col>
            </v-row>
            <v-row no-gutters justify="center">
              <v-col></v-col>
              <v-col>
                이름
                <textarea style="resize: none; width: 100%; border: 1px solid black" label="이름입력" v-model="proverb.proverbName"></textarea>
              </v-col>
              <v-col></v-col>
            </v-row>
          </v-container>

          <div class="text-center">
            <div>
              <input type="checkbox" name="success" value="success" v-model="checkbox" class="mt-2 mb-5" />
              <span class="agreement-terms" @click="showAgreement">약관</span>에 동의하십니까?
              <agreement-to-terms />
            </div>
            <v-btn style="width: 30%" x-large :loading="loading" :disabled="!checkbox" color="primary" @click="print"> 변환하기 </v-btn>
          </div>
          <div style="text-align: center; margin-top: 15px" v-if="btnHide">
            <ShareAndDownBtn :downloadLink="boardWritedownloadLink" contentType="image"></ShareAndDownBtn>
          </div>
        </v-container>
      </div>
    </div>
  </v-app>
</template>

<script>
import http from '@/util/http-common.js';
import FileUpload from '@/components/common/FileUpload.vue';
import ShareAndDownBtn from '@/components/common/ShareAndDownBtn.vue';
import Swal from 'sweetalert2';
import AgreementToTerms from '../common/AgreementToTerms.vue';

export default {
  data() {
    return {
      isHide: true,
      btnHide: false,
      previewImgUrl: '',
      downloadLink: '',
      boardWritedownloadLink: '',
      proverb: {
        //명언 내용, 이름
        proverbContent: '',
        proverbName: '',
      },
      file: {
        origin: '',
        target: '',
      },
      loader: null,
      loading: false,
      // imgPath: require('@/assets/nineone.png'),

      checkbox: false,
    };
  },
  watch: {
    loader() {
      const l = this.loader;
      this[l] = !this[l];

      setTimeout(() => (this[l] = false), 1500);

      this.loader = null;
    },
  },
  components: {
    FileUpload,
    ShareAndDownBtn,
    AgreementToTerms,
  },
  methods: {
    removeOriginImg() {
      this.file.origin = '';
    },
    removeTargetImg() {
      this.file.target = '';
    },
    originUpload(file) {
      this.previewImgUrl = URL.createObjectURL(file);
      this.isHide = false;
      //FileUpload 컴포넌트에서 #emit으로 불러서 파일전해줌
      // console.log('오리진파일 업로드');
      this.file.origin = file;
      // console.log(this.file.origin);
    },
    targetUpload(file) {
      //FileUpload 컴포넌트에서 #emit으로 불러서 파일전해줌
      // console.log('타겟파일 업로드');
      this.file.target = file;
      // console.log(this.file.target);
    },

    async print() {
      if (this.file.target == '' || this.file.origin == '') {
        Swal.fire({
          icon: 'error',
          title: '파일이 없습니다',
          width: 550,
        });
        return;
      }
      this.loader = 'loading';
      const el = this.$refs.printMe; //캔버스 들고와서
      const options = {
        type: 'dataURL',
      };

      this.output = await this.$html2canvas(el, options); //canvas에 그려서 output이 가지고 있음
      // console.log('output');
      // console.log(this.output);
      const decodImg = atob(this.output.split(',')[1]);

      let array = [];
      for (let i = 0; i < decodImg.length; i++) {
        array.push(decodImg.charCodeAt(i));
      }
      // console.log('canvas-> file 변환');
      const target = new Blob([new Uint8Array(array)], { type: 'image/jpeg' }); //canvas 값으 Blob배열형태로 저장해줌

      let formData = new FormData(); //폼데이터 만들고
      formData.append('origin', this.file.target); // 삽입할 사진
      formData.append('target', target); // 합성 당할사진

      // this.removeFile(); //파일 자동삭제

      http
        .post('/v1/deepfake', formData)
        .then((response) => {
          this.downloadLink = response.data.url + '?download=true'; //바로 다운받을 수 있게 downloadLink에다가 url넣어줌
          this.boardWritedownloadLink = response.data.url;
          // console.log(this.downloadLink);
          // console.log('성공 + 다운로드링크');
          // console.log(this.downloadLink);
          this.btnHide = true;
          Swal.fire({
            title: '변환결과!',
            imageUrl: this.downloadLink,
            imageWidth: 2000,
            imageHeight: 400,
            width: 800,

            imageAlt: 'Custom image',
          });
        })
        .catch((error) => {
          Swal.fire({
            icon: 'error',
            title: '변환실패',
            text: '권장 : 정면, 얼굴이 잘나오는 사진',
            width: 550,
          });
          // console.log('에러 + 에러내용');
          console.log(error);
          // console.log(error.response);
        });

      //파일 삭제 하기
      // this.$swal('Heading', 'this is a Heading', 'OK');
    },

    showAgreement() {
      this.$store.commit('SET_IS_AGREEMENT_TO_TERMS', true);
    },
  },
  computed: {
    extension() {
      return this.file ? this.file.name.split('.').pop() : '';
    },
    OutProverbContent() {
      return this.proverb.proverbContent.replace(/\n/g, '<br>').replace(/ /g, '&nbsp');
    },
    OutProverbName() {
      return this.proverb.proverbName.replace(/\n/g, '<br>').replace(/ /g, '&nbsp');
    },
  },
};
</script>

<style>
.hide {
  display: none;
}
.font-change {
  font-family: 'Yeon Sung', cursive;
  font-size: 2rem;
}
/* 로더 */
.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}
@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

.agreement-terms {
  color: blue;
  cursor: pointer;
}
/* 로더 */
</style>
