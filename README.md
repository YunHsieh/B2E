# B2E 測驗題目

## Simple URL Shortener
Please provide public git repository
​
1. Implement an URL shortener
  - Don’t create any fiscal cost
  - Consider all the cases in the given time frame
  - The more complete the cases you can give us, the better
​
2. Let us know how to deploy and run without asking you ANY question.
  - The app should be able to launch ANYWHERE


## URL Shortener

Get /{tinyurl}

decode將短網址貼進行會提供跳轉至該頁面。
![](https://i.imgur.com/rykd7U2.png)
直接跟model get pk 唯一值進行回傳


POST /text-to-tinyurl/

encode 將直接轉換網址
![](https://i.imgur.com/45xAtiU.png)
將會得到一組短網址

而此做法是用亂數之後進行BASE62轉換
得到6碼的短網址特徵

而如果有一樣則會先驗證之後傳遞
