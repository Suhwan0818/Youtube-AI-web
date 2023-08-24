# 유튜브 API 인공지능 웹  

```js
// Youtube_Data_Scraping_Title_Prediction

const keywords = ['컴퓨터', '강아지', '선택']

const key_search = searchByKeyword("컴퓨터")

/*
Logger.log(key_search['title'])
Logger.log(searchByVideoID(key_search['videoIDs']))
Logger.log(searchByChannelID(key_search['channelIDs']))
*/

let spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
let activeSheet = spreadSheet.getActiveSheet();

let data_scraped = dataScraper(keywords)
Logger.log(data_scraped)

activeSheet.getRange(1, 1, 1, 5).setValues([['Titles', 'VideoIDs', 'ChannelIDs', 'Views', 'Subs_count']])
activeSheet.getRange(2, 1, data_scraped.title.length, 1).setValues(data_scraped.title)
activeSheet.getRange(2, 2, data_scraped.videoIDs.length, 1).setValue(data_scraped.videoIDs)
activeSheet.getRange(2, 3, data_scraped.channelIDs.length, 1).setValue(data_scraped.channelIDs)
activeSheet.getRange(2, 4, data_scraped.views.length, 1).setValue(data_scraped.views)
activeSheet.getRange(2, 5, data_scraped.subs_count.length, 1).setValue(data_scraped.subs_count)

function dataScraper(keywords) {
  let title = [];
  let videoIDs = [];
  let channelIDs = [];
  let views = [];
  let subs_count = [];

  keywords.forEach(keyword => {
    let keyword_search = searchByKeyword(keyword)
    title.push(keyword_search.title)
    videoIDs.push(keyword_search.videoIDs)
    channelIDs.push(keyword_search.channelIDs)

    let view_results = searchByVideoID(keyword_search.videoIDs)
    views.push(view_results)

    let sub_results = searchByChannelID(keyword_search.channelIDs)
    subs_count.push(sub_results)
  })

  title = title.flat().map(x => [x])
  videoIDs = videoIDs.flat().map(x => [x])
  channelIDs = channelIDs.flat().map(x => [x])
  views = views.flat().map(x => [x])
  subs_count = subs_count.flat().map(x => [x])

  results = {
    'title' : title,
    'videoIDs' : videoIDs,
    'channelIDs' : channelIDs,
    'views' : views,
    'subs_count' : subs_count
  }
  return results
}

function searchByKeyword(keyword) {
  const results = YouTube.Search.list('id, snippet', {
    q: keyword,
    maxResults: 3
  });
  let videoIDs = results.items.map(video_info => video_info.id.videoId);
  let channelIDs = results.items.map(video_info => video_info.snippet.channelId);
  let title = results.items.map(video_info => video_info.snippet.title);
  let keyword_search = {
    'videoIDs' : videoIDs,
    'channelIDs' : channelIDs,
    'title' : title
  }
  return keyword_search
}

function searchByVideoID(videoIDs) {
  const results = YouTube.Videos.list('statistics', {
    id:videoIDs
  });
  let views = results.items.map(item => item.statistics.viewCount)
  return views
}

function searchByChannelID(channelIDs) {
  const results = channelIDs.map(channelID => YouTube.Channels.list('statistics', {
    id:channelID
  }));
  let subs_count = results.map(item => item.items[0].statistics.subscriberCount)
  return subs_count
}
```