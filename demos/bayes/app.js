import { bayesCounts } from './model.mjs';

const $ = id => document.getElementById(id);
const number = value => new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 2 }).format(value);
const percent = value => `${(value * 100).toFixed(2)}%`;
const values = { prior: 0.1, sensitivity: 99, 'false-positive': 1 };
let step = 1;
let timer = null;

function stop() {
  clearInterval(timer);
  timer = null;
  $('autoplay').textContent = '自动演示';
}

function render() {
  const c = bayesCounts(values.prior, values.sensitivity, values['false-positive']);
  const put = (id, value) => { $(id).textContent = number(value); };
  put('sick-count', c.sick); put('healthy-count', c.healthy);
  put('tp-count', c.truePositive); put('fn-count', c.falseNegative);
  put('fp-count', c.falsePositive); put('tn-count', c.trueNegative);
  $('sick-results').hidden = step < 2;
  $('healthy-results').hidden = step < 2;
  $('answer').hidden = step < 3;
  document.querySelector('.groups').classList.toggle('only-positive', step === 3);
  document.querySelectorAll('[data-step]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.step) === step)));
  const titles = ['先把10万人分成两组', '两组人，都可能测出阳性', '现在只数测出阳性的人'];
  const descriptions = [
    `患病率是${values.prior}%。10万人中，约${number(c.sick)}人患病，另外${number(c.healthy)}人没有患病。`,
    `${number(c.sick)}名患者中，${values.sensitivity}%测出阳性；${number(c.healthy)}名健康人中，${values['false-positive']}%也会测出阳性。`,
    `张三已经测出阳性，所以我们只在下面两组阳性的人里找他。阴性的人退出这次计算。`
  ];
  $('step-title').textContent = titles[step - 1];
  $('step-description').textContent = descriptions[step - 1];
  $('numerator').textContent = `${number(c.truePositive)} 名真阳性`;
  $('denominator').textContent = `${number(c.truePositive)} + ${number(c.falsePositive)} = ${number(c.positive)} 名阳性`;
  $('posterior').textContent = c.posterior === null ? '无法计算' : percent(c.posterior);
  $('true-share').style.width = `${(c.posterior ?? 0) * 100}%`;
  $('false-share').style.width = `${c.posterior === null ? 0 : (1 - c.posterior) * 100}%`;
  $('true-legend').textContent = `确实患病：${number(c.truePositive)}人`;
  $('false-legend').textContent = `没有患病：${number(c.falsePositive)}人`;
  $('positive-bar').setAttribute('aria-label', c.posterior === null ? '没有阳性结果' : `阳性人群中，${percent(c.posterior)}确实患病，其余没有患病。`);
  $('answer-explanation').textContent = c.posterior === null
    ? '按这组参数，没有人测出阳性。分母是0，阳性后患病的概率无法计算。'
    : `一共${number(c.positive)}人测出阳性，其中${number(c.truePositive)}人确实患病。所以，测出阳性后患病的概率约为${percent(c.posterior)}。${c.falsePositive > c.truePositive ? '这里的假阳性人数比真阳性人数多。假阳性率按健康人计算，健康人的基数也会影响这组人数。' : ''}`;
  $('expanded-calculation').textContent = `真阳性：100,000 × ${values.prior}% × ${values.sensitivity}% = ${number(c.truePositive)}人。假阳性：100,000 × ${number(100 - values.prior)}% × ${values['false-positive']}% = ${number(c.falsePositive)}人。`;
  $('next-step').textContent = step === 1 ? '下一步：做检测' : step === 2 ? '下一步：只看阳性的人' : '从第一步再看一遍';
}

function sync() {
  for (const [name, value] of Object.entries(values)) {
    $(name).value = value;
    $(`${name}-number`).value = value;
  }
  $('input-error').textContent = '';
  render();
}

for (const name of Object.keys(values)) {
  for (const id of [name, `${name}-number`]) {
    $(id).addEventListener('input', event => {
      const value = event.target.valueAsNumber;
      if (!Number.isFinite(value) || value < 0 || value > 100) {
        $('input-error').textContent = '请填写0到100之间的百分比。画面保留上一组有效数值。';
        return;
      }
      stop(); values[name] = value;
      const other = id === name ? `${name}-number` : name;
      $(other).value = value;
      $('input-error').textContent = '';
      render();
    });
  }
}
document.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click', () => {
  stop(); step = Number(button.dataset.step); render();
}));
$('next-step').addEventListener('click', () => { stop(); step = step === 3 ? 1 : step + 1; render(); });
$('autoplay').addEventListener('click', () => {
  if (timer) { stop(); return; }
  step = 1; render(); $('autoplay').textContent = '暂停演示';
  timer = setInterval(() => { step += 1; render(); if (step === 3) stop(); }, 2600);
});
$('book-example').addEventListener('click', () => {
  stop(); Object.assign(values, { prior: 0.1, sensitivity: 99, 'false-positive': 1 }); step = 1; sync();
});
$('higher-prior').addEventListener('click', () => { stop(); values.prior = 10; sync(); });
document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
render();
