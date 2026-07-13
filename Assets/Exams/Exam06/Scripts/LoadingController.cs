using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
namespace Exam.Exam06
{
    /// <summary>
    /// 异步加载 Game 进度条 最少四秒
    /// </summary>
    public class LoadingController : MonoBehaviour
    {
        [SerializeField] private Slider progressSlider;
        [SerializeField] private Text tipProgressText;
        [SerializeField] private float duration = 4f;

        void Start()
        {
            StartCoroutine(LoadGameRoutine());
        }

        /// <summary>
        /// 假进度+真进度 Min 双轨  满4s且 async>0.9 再激活场景
        /// </summary>
        /// <returns></returns>
        private IEnumerator LoadGameRoutine()
        {
            var op = SceneManager.LoadSceneAsync(SceneNames.Game);
            op.allowSceneActivation = false;

            float elapsed = 0f;

            while (elapsed < duration || op.progress < 0.9f)
            {
                elapsed += Time.deltaTime;

                float fakeProgress = elapsed / duration;
                float realProgress = op.progress / 0.9f;
                float disPlay = Mathf.Clamp01(Mathf.Min(fakeProgress, realProgress));

                progressSlider.value = disPlay;
                tipProgressText.text = $"加载中...{(int)(disPlay * 100)}%";

                yield return null;
            }

            progressSlider.value = 1f;
            tipProgressText.text = "加载中...100%";
            yield return new WaitForSeconds(0.3f);
            op.allowSceneActivation = true;
        }
    }
}

