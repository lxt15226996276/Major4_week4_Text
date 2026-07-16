using UnityEngine;

namespace Exam.Exam08
{
    public class PlayerSpawner : MonoBehaviour
    {
        [SerializeField] private GameObject playerPrefab;
        [SerializeField] private CameraFollow cameraFollow;

        void Start()
        {
            var player = Instantiate(playerPrefab, Vector3.zero, Quaternion.identity);
            cameraFollow.BindTarget(player.transform);
        }
    }
}

