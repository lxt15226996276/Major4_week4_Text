using UnityEngine;

namespace Exam.Exam07
{
    /// <summary>
    /// 动态生成玩家
    /// </summary>
    public class PlayerSpawner : MonoBehaviour
    {
        [SerializeField] private GameObject playerPrefab;
        [SerializeField] private CameraFollow cameraFollow;

        void Start()
        {
            var player = Instantiate(playerPrefab);
            cameraFollow.BindTarget(player.transform);
        }
    }

}
