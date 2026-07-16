using UnityEngine;
namespace Exam.Exam08
{
    public class CameraFollow : MonoBehaviour
    {
        [SerializeField] private Transform target;
        [SerializeField] private float smoothSpeed = 12f;
        private Vector3 localOffset;
        private Quaternion localRotation;

        private bool _isBound;

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

