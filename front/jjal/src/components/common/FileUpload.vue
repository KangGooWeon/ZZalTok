<template>
  <div>
    <v-container>
      <div v-if="!file" style="margin: auto; width: 50%">
        <div :class="['dropZone', dragging ? 'dropZone-over' : '']" @dragenter="dragging = true" @dragleave="dragging = false">
          <div class="dropZone-info" @drag="onChange">
            <span class="fa fa-cloud-upload dropZone-title"></span>
            <span class="dropZone-title">{{ content }} Drag&Drop</span>
            <div class="dropZone-upload-limit-info">
              <div>maximum file size: 5 MB</div>
            </div>
          </div>
          <input type="file" @change="onChange" />
        </div>
      </div>

      <div v-else class="dropZone-uploaded" style="margin: auto; width: 50%">
        <div class="dropZone-uploaded-info">
          <span class="dropZone-title">Uploaded</span>
          <button style="color: red" type="button" class="btn btn-primary removeFile" @click="removeFile">파일삭제</button>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dragging: false,
      file: '',
    };
  },
  props: {
    type: { Type: String }, //image 인지 mp4 인지
    content: { Type: String }, // 박스안에 들어갈 내용 적을 때 사용
  },
  methods: {
    // watch: {
    //   remove: function (isRemove) {
    //     console.log('리무브 변경');
    //     console.log(isRemove);
    //   },
    // },
    onChange(e) {
      var files = e.target.files || e.dataTransfer.files;

      if (!files.length) {
        this.dragging = false;
        return;
      }

      this.createFile(files[0]);
    },
    createFile(file) {
      let fileTypeSplit = file.name.split('.');
      let fileType = fileTypeSplit[1];
      // console.log(fileType);
      // console.log(typeof fileType);
      if (this.type == 'image') {
        if (fileType != 'jpg' && fileType != 'png' && fileType != 'gif' && fileType != 'jpeg') {
          alert('png, jpg, gif 파일을 넣어주세요');
          this.dragging = false;
          return;
        }
      } else if (this.type == 'video') {
        if (fileType != 'mp4') {
          alert('mp4 파일을 넣어주세요');
          this.dragging = false;
          return;
        }
      }

      if (file.size > 5000000) {
        alert('please check file size no over 5 MB.');
        this.dragging = false;
        return;
      }

      this.file = file;
      this.dragging = false;
      this.$emit('fileUpload', this.file); //파일보내줌!
    },
    removeFile() {
      this.file = '';
      if (this.type == 'image') {
        // console.log('removeiMG 에밋호출');
        this.$emit('removeImg'); //파일보내줌!
      } else if (this.type == 'video') {
        // console.log('removeVideo 에밋호출');
        this.$emit('removeVideo');
      }
    },
  },
};
</script>

<style scoped>
/****/
.dropZone {
  /* width: 50%; */
  height: 60px;
  position: relative;
  border: 2px dashed orange;
}

.dropZone:hover {
  border: 2px solid #2e94c4;
}

.dropZone:hover .dropZone-title {
  color: #1975a0;
  color: blue;
}

.dropZone-info {
  color: #a8a8a8;
  position: absolute;
  top: 50%;
  width: 100%;
  transform: translate(0, -50%);
  text-align: center;
}

.dropZone-title {
  color: blue;
}

.dropZone input {
  position: absolute;
  cursor: pointer;
  top: 0px;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
}

.dropZone-upload-limit-info {
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
}

.dropZone-over {
  background: #5c5c5c;
  opacity: 0.8;
}

.dropZone-uploaded {
  width: 100%;
  height: 60px;
  position: relative;
  border: 2px dashed red;
}

.dropZone-uploaded-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #a8a8a8;
  position: absolute;
  top: 50%;
  width: 100%;
  transform: translate(0, -50%);
  text-align: center;
}

.removeFile {
  width: 200px;
}
</style>
