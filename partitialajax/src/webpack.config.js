const path = require('path');

module.exports = {
  entry: './js/PartitialAjax.js',
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, '../static/partitialajax/'),
  },
};