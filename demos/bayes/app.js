import { bayesCounts } from './model.mjs';

const $ = id => document.getElementById(id);
const number = value => new Intl.NumberFormat('zh-CN', { maximumFractionDigits: 2 }).format(value);
const percent = value => `${(value * 100).toFixed(2)}%`;
const defaults = { prior: 0.1, sensitivity: 99, 'false-positive': 1 };
const values = { ...defaults };
const delays = { 1: 9000, 2: 12000, 3: 9000 };
let step = 2;
let mode = 'experiment';
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

function calculationLine(id, source, rate, result) {
  const parts = [`${number(source)}×`, `${rate}%=`, number(result)];
  const nodes = [];
  for (const [index, text] of parts.entries()) {
    if (index > 0) nodes.push(document.createElement('wbr'));
    const span = document.createElement('span');
    span.textContent = text;
    nodes.push(span);
  }
  $(id).replaceChildren(...nodes);
}

function render() {
  const c = bayesCounts(values.prior, values.sensitivity, values['false-positive']);
  const experiment = mode === 'experiment';
  const onlyPositive = !experiment && step === 3;
  const put = (id, value) => { $(id).textContent = number(value); };
  $('lesson').dataset.mode = mode;
  $('scene').dataset.step = experiment ? 2 : step;
  $('step-copy').hidden = experiment;
  $('back-to-experiment').hidden = experiment;
  $('step-navigation').hidden = experiment;
  $('interaction-region').hidden = !experiment;
  $('experiment-controls').hidden = !experiment;
  $('mobile-result-summary').hidden = !experiment;
  $('lesson-actions').hidden = experiment;
  $('experiment-actions').hidden = !experiment;
  $('playback-settings').hidden = experiment;
  $('after-lesson').hidden = !experiment && step !== 4;
  $('population').hidden = experiment || step > 2;
  $('groups').hidden = !experiment && step === 4;
  $('counts-title').hidden = !experiment;
  $('counts-intro').hidden = !experiment;
  for (const id of ['sick-derivation', 'healthy-derivation']) $(id).hidden = !experiment && step > 2;
  for (const id of ['sick-explanation', 'healthy-explanation']) $(id).hidden = !experiment;
  for (const id of ['sick-origin', 'healthy-origin', 'sick-source', 'healthy-source']) $(id).hidden = onlyPositive;
  $('sick-results').hidden = !experiment && step === 1;
  $('healthy-results').hidden = !experiment && step === 1;
  for (const id of ['sick-transform', 'healthy-transform']) $(id).hidden = !experiment && step !== 2;
  for (const id of ['sick-negative', 'healthy-negative']) $(id).hidden = experiment || step !== 2;
  $('answer').hidden = !experiment && step !== 4;

  put('sick-count', c.sick); put('healthy-count', c.healthy);
  put('tp-count', c.truePositive); put('fp-count', c.falsePositive);
  $('population-explanation').textContent = `患病率是${values.prior}%，也就是每1000人中约有${number(values.prior * 10)}人患病。放到这10万人中，就是100,000×${values.prior}%=${number(c.sick)}名患者，剩下${number(c.healthy)}人没有患病。`;
  $('counts-intro').textContent = `先按患病比例把10万人分成患者和健康人，再分别对这两组人做检测。下面每一组都写出起始人数、检测比例和阳性人数。${[c.sick,c.healthy,c.truePositive,c.falsePositive].some(n=>Math.abs(n-Math.round(n))>1e-8) ? '这里按比例计算平均人数；人数带小数，表示多次同样检测的平均结果。' : ''}`;
  $('sick-derivation').textContent = `先算患者人数：100,000×${values.prior}%=${number(c.sick)}人。`;
  $('healthy-derivation').textContent = `其余人没有患病：100,000−${number(c.sick)}=${number(c.healthy)}人。`;
  $('sick-explanation').textContent = `这${number(c.sick)}名患者中，有${values.sensitivity}%会测出阳性，所以得到${number(c.truePositive)}人。他们确实患病，也测出阳性，叫“真阳性”；另外${number(c.falseNegative)}人测出阴性。`;
  $('healthy-explanation').textContent = `这${number(c.healthy)}名健康人中，有${values['false-positive']}%会被误判为阳性，所以得到${number(c.falsePositive)}人。他们没有患病，却测出阳性，叫“假阳性”；另外${number(c.trueNegative)}人测出阴性。`;
  $('sick-label').textContent = onlyPositive ? '确实患病，也测出阳性' : '实际患病';
  $('healthy-label').textContent = onlyPositive ? '没有患病，却测出阳性' : '没有患病';
  $('sick-rate').textContent = `其中${values.sensitivity}%测出阳性`;
  $('healthy-rate').textContent = `其中${values['false-positive']}%被误判`;
  calculationLine('sick-calculation', c.sick, values.sensitivity, c.truePositive);
  calculationLine('healthy-calculation', c.healthy, values['false-positive'], c.falsePositive);
  $('tp-label').textContent = onlyPositive ? '确实患病，也测出阳性' : '测出阳性';
  $('fp-label').textContent = onlyPositive ? '没有患病，却测出阳性' : '被误判为阳性';
  $('tp-note').textContent = onlyPositive ? `真阳性 · 从${number(c.sick)}名患者中测出` : '真阳性';
  $('fp-note').textContent = onlyPositive ? `假阳性 · 从${number(c.healthy)}名健康人中测出` : '假阳性';
  $('sick-negative').textContent = `这${number(c.sick)}名患者中，另外${number(c.falseNegative)}人测出阴性。`;
  $('healthy-negative').textContent = `这${number(c.healthy)}名健康人中，另外${number(c.trueNegative)}人测出阴性。`;
  $('scene-note').textContent = experiment ? '' : step === 1 ? '两组人数相加，仍然是最开始的10万人。' : step === 2 ? '两组人里都出现了阳性。下一步，我们只看这些阳性的人。' : step === 3 ? '阴性的人退出计算。接下来，只把这两组阳性的人加起来。' : '';

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
  $('next-step').textContent = ['下一步：做检测', '下一步：只看阳性的人', '下一步：算出概率', '回到交互实验'][step - 1];

  $('numerator').textContent = number(c.truePositive);
  $('denominator').textContent = `${number(c.truePositive)} + ${number(c.falsePositive)}`;
  $('posterior').textContent = c.posterior === null ? '无法计算' : percent(c.posterior);
  $('summary-posterior').textContent = $('posterior').textContent;
  $('summary-tp').textContent = `患者测出阳性：${number(c.truePositive)}人`;
  $('summary-fp').textContent = `健康人被误判：${number(c.falsePositive)}人`;
  $('positive-total-explanation').textContent = c.positive === 0 ? '两组阳性人数都是0，0＋0＝0。这组参数下没有人测出阳性，无法继续计算阳性后患病的概率。' : `把上面两组阳性的人加起来：${number(c.truePositive)}名患者＋${number(c.falsePositive)}名被误判的健康人＝${number(c.positive)}人。我们已经知道检测结果是阳性，接下来只看这${number(c.positive)}人中，有多少人确实患病。`;
  $('approximately').hidden = c.posterior === null;
  document.querySelector('.answer-equation').setAttribute('aria-label', c.posterior === null ? '阳性人数为0，分母为0，无法计算。' : `${number(c.truePositive)}名真阳性，除以全部${number(c.positive)}名阳性，约为${percent(c.posterior)}。`);
  $('answer-explanation').textContent = c.posterior === null
    ? '按这组参数，没有人测出阳性。分母是0，阳性后患病的概率无法计算。'
    : `在这${number(c.positive)}名阳性的人中，确实患病的是${number(c.truePositive)}人。用${number(c.truePositive)}除以${number(c.positive)}，得到${percent(c.posterior)}。这就是测出阳性后患病的概率。`;
  $('denominator-explanation').querySelector('summary').textContent = `“患者中有${values.sensitivity}%测出阳性”和“阳性后患病的概率”，分母为什么不同？`;
  document.querySelector('.positive-composition').hidden = c.posterior === null;
  $('true-share').style.width = `${(c.posterior ?? 0) * 100}%`;
  $('false-share').style.width = `${c.posterior === null ? 0 : (1 - c.posterior) * 100}%`;
  $('true-legend').textContent = `确实患病：${number(c.truePositive)}人`;
  $('false-legend').textContent = `没有患病：${number(c.falsePositive)}人`;
  $('positive-bar').setAttribute('aria-label', c.posterior === null ? '没有阳性结果' : `测出阳性的${number(c.positive)}人中，${number(c.truePositive)}人确实患病，占${percent(c.posterior)}；${number(c.falsePositive)}人没有患病。`);
  $('comparison-explanation').textContent = `“能查出${values.sensitivity}%的患者”，先选中已经患病的人，再看检测结果。“阳性后患病的概率”先选中已经测出阳性的人，再看谁患病。前者的分母是全部患者，后者的分母是全部阳性的人。`;
  $('expanded-calculation').textContent = `真阳性人数：100,000 × ${values.prior}% × ${values.sensitivity}% = ${number(c.truePositive)}人。假阳性人数：100,000 × ${number(100 - values.prior)}% × ${values['false-positive']}% = ${number(c.falsePositive)}人。`;
  $('current-method').textContent = `当前设置：${values.sensitivity}%的患者会测出阳性，${values['false-positive']}%的健康人会被误判为阳性。`;
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
  stop(); mode = 'experiment'; render(); scrollToLesson();
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
  stop(); mode = 'lesson'; step = 1; sync(); scrollToLesson();
});
$('back-to-experiment').addEventListener('click', () => {
  stop(); mode = 'experiment'; step = 2; render(); scrollToLesson();
});
document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
render();
document.documentElement.dataset.labReady = 'true';
