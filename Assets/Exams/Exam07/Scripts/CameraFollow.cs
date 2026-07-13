using UnityEngine;
namespace Exam.Exam07
{
    /// <summary>
    /// 相机跟随，提前调整好相机与玩家的初始距离和方向
    /// </summary>
    public class CameraFollow : MonoBehaviour
    {
        [SerializeField] private Transform target;
        [SerializeField] private float smoothSpeed = 12f;
        private Vector3 localOffset;
        private Quaternion localRotation;

        private bool _isBound;
        /// <summary>
        /// 玩家生成时设置相机跟随
        /// </summary>
        /// <param name="player"></param>
        public void BindTarget(Transform player)
        {
            target = player;
            localOffset = target.InverseTransformPoint(transform.position);
            localRotation = Quaternion.Inverse(target.rotation) * transform.rotation;
            _isBound = true;
        }

        void LateUpdate()
        {
            if (!_isBound || target == null) return;

            var pos = target.TransformPoint(localOffset);
            var rotation = target.rotation * localRotation;

            transform.position = Vector3.Lerp(transform.position, pos, smoothSpeed * Time.deltaTime);
            transform.rotation = Quaternion.Slerp(transform.rotation, rotation, smoothSpeed * Time.deltaTime);
        }

    }
}
