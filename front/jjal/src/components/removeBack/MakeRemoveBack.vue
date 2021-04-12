<template>
  <div id="container">
    <div><v-img src="@/assets/banner3.png" alt="" max-width="100%" max-height="300px" /></div>
    <v-container>
      <v-container v-if="isTransfer">
        {{ video.sources.src }}
        <div class="videoContainer" style="margin: auto">
          <my-video :sources="video.sources" :options="video.options"></my-video>
        </div>
      </v-container>

      <div>
        <FileUpload type="image" v-on:fileUpload="removeBackImgUpload" v-on:removeImg="removeImg" content="배경 이미지"></FileUpload>
        <FileUpload type="video" v-on:fileUpload="removeBackVideoUpload" v-on:removeVideo="removeVideo" content="배경제거동영상"></FileUpload>
      </div>
      <div style="text-align: center">
        <div>
          <input type="checkbox" name="success" value="success" v-model="checkbox" class="mt-2 mb-5" />
          <span class="agreement-terms ml-2" @click="showAgreement">약관</span>에 동의하십니까?
          <agreement-to-terms />
        </div>
        <v-btn style="width: 30%" x-large color="primary" @click="transfer" :disabled="!checkbox"> 변환하기 </v-btn>
      </div>
      <div style="text-align: center; margin-top: 15px" v-if="btnHide">
        <ShareAndDownBtn :downloadLink="downloadLink" contentType="video"></ShareAndDownBtn>
      </div>
    </v-container>
  </div>
</template>

<script>
import myVideo from 'vue-video';
import FileUpload from '@/components/common/FileUpload.vue';
import ShareAndDownBtn from '@/components/common/ShareAndDownBtn.vue';
import http from '@/util/http-common.js';
import AgreementToTerms from '../common/AgreementToTerms.vue';
import Swal from 'sweetalert2';

export default {
  components: { myVideo, FileUpload, ShareAndDownBtn, AgreementToTerms },
  data() {
    return {
      isHide: true,
      btnHide: false,
      isTransfer: false,
      removeBackImg: '',
      removeBackVideo: '',
      downloadLink: '',
      video: {
        sources: [
          {
            src: '',
            type: 'video/mp4',
          },
        ],
        options: {
          controls: true,
          muted: true,
          poster: '',
          autoplay: true,
        },
      },

      checkbox: false,
    };
  },

  methods: {
    removeImg() {
      this.removeBackImg = '';
    },
    removeVideo() {
      this.removeBackVideo = '';
    },
    async httpCall(formData) {
      await http
        .post('/v1/removeBg', formData)
        .then((response) => {
          this.video.sources.splice(0, 1);
          this.downloadLink = response.data.url;
          this.video.sources.push({ src: this.downloadLink, type: 'video/mp4' });
          Swal.close();
          Swal.fire({
            icon: 'success',
            title: '변환완료',
            showConfirmButton: false,
            timer: 1000,
          });
          this.btnHide = true;
          this.isTransfer = true;
        })
        .catch((error) => {
          // console.log('에러요');
          console.log(error);
          // console.log(error.response);
        });

      return true;
    },
    async transfer() {
      this.isTransfer = false;
      if (this.removeBackImg == '' || this.removeBackVideo == '') {
        Swal.fire({
          icon: 'error',
          title: '파일이 없습니다',
          width: 550,
        });
        return;
      }
      // console.log('배경교체 변환시작');
      let formData = new FormData();
      formData.append('video', this.removeBackVideo);
      formData.append('image', this.removeBackImg);

      await Swal.fire({
        title: '변환중',
        html: '약 10초~30초정도 소요됩니다.',
        timer: 10000000,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading();

          if (this.httpCall(formData)) {
            // console.log('????');
          }
        },
        willClose: () => {
          clearInterval();
        },
      }).then((result) => {
        /* Read more about handling dismissals below */
        if (result.dismiss === Swal.DismissReason.timer) {
          // console.log('I was closed by the timer');
        }
      });
    },
    removeBackImgUpload(file) {
      this.removeBackImg = file;
      // console.log(file);
    },
    removeBackVideoUpload(file) {
      this.removeBackVideo = file;
      // console.log(file);
    },
    showAgreement() {
      this.$store.commit('SET_IS_AGREEMENT_TO_TERMS', true);
    },
  },
  computed: {},
};
</script>

<style scoped>
.videoContainer {
  width: 50%;
  /* min-width: 600px; */
  height: 80%;
}

.input-file-button {
  padding: 6px 25px;
  background-color: #ff6600;
  border-radius: 10px;
  color: white;
  cursor: pointer;
}

#preview img {
  max-width: 100%;
}

.__cov-contrl-content {
  z-index: 1;
}
</style>
