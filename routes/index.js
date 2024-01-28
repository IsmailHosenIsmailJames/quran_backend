var express = require("express");
var router = express.Router();
var path = require("path");
const fs = require("fs");


/* GET home page. */
router.get("/", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/index.html"));
});

router.get("/languages", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/languages.json"));
});

router.get("/chapter_infos", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/chapter_infos.json"));
});

router.get("/translations", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/translations.json"));
});

router.get("/tafsirs_info", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/tafsirs.json"));
});

router.get("/list_of_resource_tafseer", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/list_of_resource_tafseer.json"));
});

router.get("/juzs", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/juzs.json"));
});

router.get("/tafsirs", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/tafsirs.json"));
});

router.get("/chapters", function (req, res, next) {
  res.sendFile(path.join(__dirname, "/../public/chapters.json"));
});

router.get("/tafseer/:id", function (req, res, next) {
  const id = req.params.id;
  const filePath = path.join(__dirname, "/../public/tafseer/", id + ".json");

  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      res.status(404).send("Chapter not found");
    } else {
      res.sendFile(filePath);
    }
  });
});

router.get("/quran/:name", function (req, res, next) {
  const name = req.params.name;
  const filePath = path.join(__dirname, "/../public/quran/", name + ".json");

  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      res.status(404).send("Chapter not found");
    } else {
      res.sendFile(filePath);
    }
  });
});

router.get("/translation/:id", function (req, res, next) {
  const id = req.params.id;
  const filePath = path.join(__dirname, "/../public/translation/", id + ".json");

  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      res.status(404).send("id not found");
    } else {
      res.sendFile(filePath);
    }
  });
});

module.exports = router;
