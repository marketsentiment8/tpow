// 2_TPOW_migration.js

const Migrations = artifacts.require("TrainingPoW");

module.exports = function (deployer){
  deployer.deploy(Migrations);
}