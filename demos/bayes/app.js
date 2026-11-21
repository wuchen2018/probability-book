import { bayesCounts } from './model.mjs';

const $ = id => document.getElementById(id);
const number = value => new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 2 }).format(value);
const percent = value => `${(value * 100).toFixed(2)}%`;
const defaults = { prior: 0.1, sensitivity: 99, 'false-positive': 1 };
const values = { ...defaults };
const delays = { 1: 9000, 2: 12000, 3: 9000 };
const smallScreen = matchMedia('(max-width: 700px)');
let step = 1;
let mode = 'lesson';
let playing = false;
let timer = null;

function playbackLabel() {
  $('autoplay').textContent = playing ? '暂停播放' : step === 4 ? '从头自动播放' : step === 1 ? '开始自动播放' : '继续自动播放';
}

function stop() {
  clearTimeout(timer);
  timer = null;
  playing = false;
  playbackLabel();
}

function scrollToLesson() {
  $('lesson').scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
}

function render() {
  const c = bayesCounts(values.prior, values.sensitivity, values['false-positive']);
  const experiment = mode === 'experiment';
  const put = (id, value) => { $(id).textContent = number(value); };
  $('lesson').dataset.mode = mode;
  $('scene').dataset.step = step;
  $('step-navigation').hidden = experiment;
  $('experiment-controls').hidden = !experiment;
  $('mobile-result-summary').hidden = !experiment || !smallScreen.matches;
  $('lesson-actions').hidden = experiment;
  $('experiment-actions').hidden = !experiment;
  $('playback-settings').hidden = experiment;
  $('after-lesson').hidden = step !== 4;
  $('population').hidden = step > 2;
  $('groups').hidden = step === 4;
  $('sick-origin').hidden = step === 3;
  $('healthy-origin').hidden = step === 3;
  $('sick-source').hidden = step === 3;
  $('healthy-source').hidden = step === 3;
  $('sick-results').hidden = step === 1;
  $('healthy-results').hidden = step === 1;
  for (const id of ['sick-transform', 'healthy-transform', 'sick-negative', 'healthy-negative']) $(id).hidden = step !== 2;
  $('answer').hidden = step !== 4;

  put('sick-count', c.sick); put('healthy-count', c.healthy);
  put('tp-count', c.truePositive); put('fp-count', c.falsePositive);
  $('sick-label').textContent = step === 3 ? '确实患病，也测出阳性' : '实际患病';
  $('healthy-label').textContent = step === 3 ? '没有患病，却测出阳性' : '没有患病';
  $('sick-rate').textContent = `其中${values.sensitivity}%测出阳性`;
  $('healthy-rate').textContent = `其中${values['false-positive']}%被误判`;
  $('sick-calculation').textContent = `${number(c.sick)}×${values.sensitivity}%=${number(c.truePositive)}`;
  $('healthy-calculation').textContent = `${number(c.healthy)}×${values['false-positive']}%=${number(c.falsePositive)}`;
  $('tp-label').textContent = step === 3 ? '确实患病，也测出阳性' : '测出阳性';
  $('fp-label').textContent = step === 3 ? '没有患病，却测出阳性' : '被误判为阳性';
  $('tp-note').textContent = step === 3 ? `真阳性 · 从${number(c.sick)}名患者中测出` : '真阳性';
  $('fp-note').textContent = step === 3 ? `假阳性 · 从${number(c.healthy)}名健康人中测出` : '假阳性';
  $('sick-negative').textContent = `这${number(c.sick)}名患者中，另外${number(c.falseNegative)}人测出阴性。`;
  $('healthy-negative').textContent = `这${number(c.healthy)}名健康人中，另外${number(c.trueNegative)}人测出阴性。`;
  $('scene-note').textContent = step === 1 ? '两组人数相加，仍然是最开始的10万人。' : step === 2 ? '两组人里都出现了阳性。下一步，我们只看这些阳性的人。' : step === 3 ? '阴性的人退出计算。接下来，只把这两组阳性的人加起来。' : '';

  const titles = ['先把10万人分成两组', '给两组人做检测', '现在，只看测出阳性的人', '分母只数测出阳性的人'];
  const descriptions = [
    `患病率是${values.prior}%，也就是每1000人中约有${number(values.prior * 10)}人患病。10万人中，约${number(c.sick)}人患病，另外${number(c.healthy)}人没有患病。`,
    `给两组人用同一种方法做检测。患者中${values.sensitivity}%测出阳性；健康人中${values['false-positive']}%也会测出阳性。分别乘一下，看看各有多少人。`,
    '张三已经测出阳性。他可能确实患病，也可能没有患病、被误判为阳性。我们就在这两组人里找他。',
    `两组阳性的人加起来，${number(c.truePositive)} + ${number(c.falsePositive)} = ${number(c.positive)}人。现在问：其中确实患病的${number(c.truePositive)}人，占多少？`
  ];
  $('step-label').textContent = experiment ? '自己试一试' : `第${step}步 / 共4步`;
  $('step-title').textContent = experiment ? '你来改一改，看看人数怎样变化' : titles[step - 1];
  $('step-description').textContent = experiment ? '先只改变患病率，观察真阳性、假阳性的人数和最后的概率。需要时，再展开下面的设置，改变检测方法。' : descriptions[step - 1];
  document.querySelectorAll('#step-navigation [data-step]').forEach(button => {
    if (Number(button.dataset.step) === step) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
  });
  $('previous-step').disabled = step === 1;
  $('next-step').textContent = ['下一步：做检测', '下一步：只看阳性的人', '下一步：算出概率', '自己改一改患病率'][step - 1];

  $('numerator').textContent = number(c.truePositive);
  $('denominator').textContent = `${number(c.truePositive)} + ${number(c.falsePositive)}`;
  $('posterior').textContent = c.posterior === null ? '无法计算' : percent(c.posterior);
  $('summary-posterior').textContent = $('posterior').textContent;
  $('summary-tp').textContent = `真阳性 ${number(c.truePositive)}人`;
  $('summary-fp').textContent = `假阳性 ${number(c.falsePositive)}人`;
  $('approximately').hidden = c.posterior === null;
  document.querySelector('.answer-equation').setAttribute('aria-label', c.posterior === null ? '阳性人数为0，分母为0，无法计算。' : `${number(c.truePositive)}名真阳性，除以全部${number(c.positive)}名阳性，约为${percent(c.posterior)}。`);
  $('answer-explanation').textContent = c.posterior === null
    ? '按这组参数，没有人测出阳性。分母是0，阳性后患病的概率无法计算。'
    : `${number(c.positive)}人测出阳性，其中${number(c.truePositive)}人确实患病。所以，测出阳性后患病的概率约为${percent(c.posterior)}。`;
  document.querySelector('.positive-composition').hidden = c.posterior === null;
  $('true-share').style.width = `${(c.posterior ?? 0) * 100}%`;
  $('false-share').style.width = `${c.posterior === null ? 0 : (1 - c.posterior) * 100}%`;
  $('true-legend').textContent = `确实患病：${number(c.truePositive)}人`;
  $('false-legend').textContent = `没有患病：${number(c.falsePositive)}人`;
  $('positive-bar').setAttribute('aria-label', c.posterior === null ? '没有阳性结果' : `测出阳性的${number(c.positive)}人中，${number(c.truePositive)}人确实患病，占${percent(c.posterior)}；${number(c.falsePositive)}人没有患病。`);
  $('comparison-explanation').textContent = `“能查出${values.sensitivity}%的患者”，先选中已经患病的人，再看检测结果。张三的问题先选中已经测出阳性的人，再看谁患病。前者的分母是全部患者，后者的分母是全部阳性的人。`;
  $('expanded-calculation').textContent = `真阳性人数：100,000 × ${values.prior}% × ${values.sensitivity}% = ${number(c.truePositive)}人。假阳性人数：100,000 × ${number(100 - values.prior)}% × ${values['false-positive']}% = ${number(c.falsePositive)}人。`;
  $('current-method').textContent = `当前检测方法：${values.sensitivity}%的患者会测出阳性，${values['false-positive']}%的健康人会被误判为阳性。`;
  playbackLabel();
}

function sync() {
  for (const [name, value] of Object.entries(values)) {
    $(name).value = value;
    $(`${name}-number`).value = value;
  }
  $('input-error').textContent = '';
  render();
}

function schedule() {
  clearTimeout(timer);
  if (!playing || step === 4) { stop(); return; }
  timer = setTimeout(() => {
    step += 1; render();
    if (step === 4) stop(); else schedule();
  }, delays[step] * Number($('pace').value));
}

function setStep(nextStep) {
  stop(); step = Math.max(1, Math.min(4, nextStep)); render(); scrollToLesson();
}

for (const name of Object.keys(values)) {
  for (const id of [name, `${name}-number`]) {
    $(id).addEventListener('input', event => {
      const value = event.target.valueAsNumber;
      if (!Number.isFinite(value) || value < 0 || value > 100) {
        $('input-error').textContent = '请填写0到100之间的百分比。画面保留上一组有效数值。';
        return;
      }
      values[name] = value;
      $(id === name ? `${name}-number` : name).value = value;
      $('input-error').textContent = '';
      render();
    });
  }
}
document.querySelectorAll('#step-navigation [data-step]').forEach(button => button.addEventListener('click', () => setStep(Number(button.dataset.step))));
$('previous-step').addEventListener('click', () => setStep(step - 1));
$('next-step').addEventListener('click', () => {
  if (step < 4) { setStep(step + 1); return; }
  stop(); mode = 'experiment'; $('playback-settings').open = false; render(); scrollToLesson();
});
$('autoplay').addEventListener('click', () => {
  if (playing) { stop(); return; }
  if (step === 4) { step = 1; render(); }
  playing = true; playbackLabel(); scrollToLesson(); schedule();
});
$('pace').addEventListener('change', () => { if (playing) schedule(); });
$('playback-settings').querySelector('summary').addEventListener('click', () => { if ($('playback-settings').open) stop(); });
$('playback-settings').addEventListener('toggle', () => { if (!$('playback-settings').open) stop(); });
$('book-example').addEventListener('click', () => { Object.assign(values, defaults); sync(); });
$('higher-prior').addEventListener('click', () => { values.prior = 10; sync(); });
$('back-to-lesson').addEventListener('click', () => {
  stop(); mode = 'lesson'; step = 1; Object.assign(values, defaults); $('method-settings').open = false; sync(); scrollToLesson();
});
document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
smallScreen.addEventListener('change', render);
render();
document.documentElement.dataset.labReady = 'true';
