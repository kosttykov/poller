const hoursNode = document.querySelector('.hr');
const minutesNode = document.querySelector('.mn');
const secondsNode = document.querySelector('.sc');
const sendBtn = document.querySelector('#sendbtn');

let time = 10;
let nIntervId = null;

const numberConverter = (value) => {
  if (value < 10) {
    return `0${value}`;
    // return '0' + value;
  }
  return `${value}`;
  // return '' + value;
}

const changeTimerTime = () => {
  const hours = Math.floor(time / 60 / 60);
  const minutes = Math.floor((time - hours * 60 * 60) / 60);
  const seconds = time - hours * 60 * 60 - minutes * 60;
  
  hoursNode.innerHTML = numberConverter(hours);
  minutesNode.innerHTML = numberConverter(minutes);
  secondsNode.innerHTML = numberConverter(seconds);
}

changeTimerTime();

document.addEventListener('DOMContentLoaded', () => {
  console.log('nIntervId', nIntervId)

  if (!nIntervId && time > 0) {
    nIntervId = setInterval(() => {
      console.log('hello')
      if (time > 0) {
        time = time - 1;
        changeTimerTime();
      } else {
        clearInterval(nIntervId);
        nIntervId = null;
        console.log('IM done!!!!')
        sendBtn.click()
      }
    }, 1000); 
  }
});
