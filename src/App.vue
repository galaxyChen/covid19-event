<template>
  <el-container>
    <el-header>
      <div class="header">
      <a>新冠肺炎大事记</a>
    </div>
    </el-header>

    <el-main>
      <div class="time">
      <el-row justify="center" type="flex">
        <el-col :span="2">
          <i class="arrow el-icon-back" @click="goLast"></i>
        </el-col>
        <el-col :span="6" style="width:fit-content;">
          <el-date-picker
            class="picker"
            v-model="date_picker"
            type="date"
            placeholder="选择日期"
            @change="changeDate"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-col>
        <el-col style="text-align:right;" :span="2">
          <i class="arrow el-icon-right" @click="goNext"></i>
        </el-col>
      </el-row>
    </div>

    <div class="main">
      <div class="news">
        <el-carousel
          ref="news"
          height="200px"
          :autoplay="false"
          @change="onChange"
          :loop="false"
          indicator-position="none"
          :initial-index="active"
        >
          <el-carousel-item class="news-item" v-for="(item, index) in news" :key="index">
            <div class="news-card">
              <h3 class="news-date">{{dates[index]}}</h3>
              <p class="news-text">{{item}}</p>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>

      <div class="pic">
        <el-carousel
          ref="pic"
          height="400px"
          :autoplay="false"
          :loop="false"
          indicator-position="none"
          :initial-index="active"
          arrow="never"
        >
          <el-carousel-item class="pic-item" v-for="(item, index) in pics" :key="index">
            <div class="picture" v-if="item==''"></div>
            <img class="picture" v-else :src="item" />
            <!-- <img class="picture" src="./assets/01-19.png" /> -->
          </el-carousel-item>
        </el-carousel>
      </div>
    </div>
    </el-main>

    <el-footer class="footer">
      <span style="text-align:center;">
        <p class="footer-text">本网站由上海交通大学2019新冠肺炎抗疫大事记实践团制作</p>
        <p class="footer-text">不忘初心,牢记使命</p>
      </span>
      <img class="footer-img" src="https://www.sjtu.edu.cn/resource/assets/img/LogoWhite.png"/>
      
      
    </el-footer>
  </el-container>
</template>

<script>
import axios from "axios";

export default {
  async mounted() {
    let begin = "2019-12-01";
    let end = "2020-01-23";
    let init_data = await axios.get(`/getNews?begin=${begin}&end=${end}`);
    // let init_data = {
    //   'news':[],
    //   'dates':[],
    //   'pics':[]
    // }
    if (init_data.status == 200) {
      this.news = init_data["data"]["news"];
      this.dates = init_data["data"]["dates"];
      this.pics = init_data["data"]["pics"];
      this.date_picker = "2020-01-19";
      this.active = 77;
    }
  },
  data() {
    return {
      news: [],
      dates: [],
      pics: [],
      active: 0,
      date_picker: "2019-12-01",
    };
  },
  methods: {
    onChange(current) {
      this.active = current;
      this.date_picker = this.dates[current];
      if (current > this.news.length / 2) {
        let date = new Date(this.dates[this.dates.length - 1]);
        date.setDate(date.getDate() + 1);
        axios
          .get("/getOneNews?date=" + date.toISOString().slice(0, 10))
          .then((res) => {
            if (
              res.status == 200 &&
              JSON.stringify(res.data) != "{}" &&
              res.data["news"] != ""
            ) {
              this.news.push(res.data["news"]);
              this.dates.push(res.data["date"]);
              this.pics.push(res.data["pics"]);
            }
          });
      }
    },
    changeDate(date) {
      if (date < "2019-12-01") date = "2019-12-01";
      let today = new Date();
      today = today.toISOString().slice(0, 10);
      if (date > today) date = today;
      let latestDate = this.dates[this.dates.length - 1];
      if (latestDate < date) {
        axios.get(`/getNews?begin=2019-12-01&end=${date}`).then((res) => {
          this.news = res["data"]["news"];
          this.dates = res["data"]["dates"];
          this.pics = res["data"]["pics"];
          this.date_picker = this.dates[this.dates.length - 1];
          this.active = this.news.length - 1;
        });
      } else {
        for (let i = 0; i < this.dates.length; i++) {
          if (this.dates[i] >= date) {
            console.log(date);
            console.log(i);
            this.active = i;
            this.$refs.pic.setActiveItem(i);
            this.$refs.news.setActiveItem(i);
            this.date_picker = this.dates[i];
            break;
          }
        }
      }
    },
    goLast() {
      this.$refs.news.prev();
      this.$refs.pic.prev();
    },
    goNext() {
      this.$refs.news.next();
      this.$refs.pic.next();
    },
  },
};
</script>

<style>
body {
  margin: 0;
  background-color: rgb(249, 249, 249);
}

.footer-img {
  background-color: red;
}

.main {
  /* background-image: url('https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3114336894,3869751630&fm=26&gp=0.jpg'); */
  /* background-size: 100% 100%;
  background-repeat: no-repeat; */
}

.time {
  margin-top: 20px;
}

.picker {
  text-align: center;
}

.arrow {
  font-size: 32px;
  line-height: 40px;
}

.news {
  height: 200px;
  width: 60%;
  margin: 0 auto;
  margin-top: 30px;
}

.news-card {
  height: 100%;
  width: 100%;
  overflow: auto;
  overflow-x: hidden;
  background-color: white;
}

.news-date {
  padding-left: 10px;
}

.news-text {
  padding: 0 10px;
}

.pic {
  width: 50%;
  margin: 0 auto;
  margin-top: 20px;
  text-align: center;
}

.picture {
  height: 384px;
  width: 512px;
}

.header {
  color: white;
  height: 40px;
  line-height: 40px;
  font-size: 24px;
  background-color: #b3c0d1;
  padding-left: 10px;
  margin: 0;
}

.footer {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.footer-text {
  margin: 0;
  margin-bottom: 5px;
  color: #909399;
}
</style>