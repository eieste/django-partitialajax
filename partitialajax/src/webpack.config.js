const path = require('path');

module.exports = {
  entry: './js/PartitialAjax.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, '../static/ajaxpartitial/'),
  },
};