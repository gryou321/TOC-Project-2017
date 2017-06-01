# TOC Project 2017
###### tags: `Chatbot` `Telegram` `Python3`

## 作業目標
* 在 `Telegram` 的平台上建立簡易的聊天機器人，根據自己設計的 FSM 圖設計出相對應的聊天機器人，並且使用 `Python3` 實作
## Setup
### Prerequisite
* Python 3
### Other packages
* Flask (後端)
* transitions (做出 FSM 圖)
* pygraphviz (畫出 FSM 圖)
* python-telegram-bot (聊天機器人)
* requests (爬蟲)
* bs4 (爬蟲)

## Finite State Machine

## 操作說明
* initial state 為 `init`
* 之後分成三種不同的路徑 : `Hello`, `Goodbye`, `Weather` ，各路徑的最後會回到 `init`

    * `Hello` : 當輸入"Hello"或"Hi"時，狀態進入 `Hello`，機器人會隨機回應以下四句 :
        
        > 你好
        
        > 哈囉
        
        > Hi
        
        > Hello
        
        然後狀態再度回到 `init`
    
    
    * `Goodbye` : 當輸入"Goodbye"或"Bye"時，狀態進入 `Goodbye`，機器人會隨機回應以下四句 :
         >掰掰
         
         >再見
         
         >Goodbye
         
         >Bye~
         
         然後狀態再度回到 `init`
         
    * `Weather` : 共分成三個階段: `Weather1`, `Weather2`, `Weather3` ：
        * 當輸入"天氣"時，會進入 `Weather1`，並且機器人會回應 :
            > 你想問哪個縣市的天氣呢?
        * 當輸入縣市名稱時，如果正確的話，會進入 `Weather2`，並且機器人會回應 :

            > 你想問哪個時段的天氣呢( 1 : 最近6小時 / 2 : 6小時之後 / 3 : 12小時之後)

            如果輸入錯誤的名稱，則會回應 :
            > "台灣沒有這個縣市喔"
             
            狀態停留在`Weather1`
        * 當輸入時段時，如果正確的話，會進入 `Weather3`， 並且機器人會回應 :
            > 地點:XXX
時間:XXXX XX/XX XX:00~XX:00 
溫度:XX~XX 
濕度:XX% 
天氣狀況:(根據氣象局網站的資料而定)


            如果輸入錯誤的名稱，則會回應 :
            > "輸入時段錯誤!!??"
			
			狀態停留在 `Weather2`
            
        * 當狀態進入 `Weather3` 後，狀態會直接回到 `init`