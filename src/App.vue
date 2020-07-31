<template>
  <div>
    <div class="header">
      <a>新冠肺炎大事记</a>
    </div>

    <div class="news">
      <el-carousel
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
          <div class="picture" v-if='item==""'></div>
          <img class="picture" v-else :src="item" />
          <!-- <img class="picture" src="./assets/01-19.png" /> -->
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  async mounted() {
    let begin = "2019-12-01";
    let end = "2019-12-13";
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
    }
  },
  data() {
    return {
      news: [],
      dates: [],
      pics: [],
      active: 0,
    };
  },
  methods: {
    onChange(current) {
      this.active = current;
      this.$refs.pic.setActiveItem(current);
      if (current > this.news.length / 2) {
        let date = new Date(this.dates[this.dates.length - 1]);
        date.setDate(date.getDate() + 1);
        axios
          .get("/getOneNews?date=" + date.toISOString().slice(0, 10))
          .then((res) => {
            if (res.status == 200 && JSON.stringify(res.data)!="{}" && res.data["news"] != "") {
              this.news.push(res.data["news"]);
              this.dates.push(res.data["date"]);
              this.pics.push(res.data["pics"]);
            }
          });
      }
    },
  },
};
</script>

<style>
body {
  margin: 0;
  background-color: rgb(249, 249, 249);
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
</style>