using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//*****************************************
//创建人： Trigger 
//功能说明：特效销毁
//***************************************** 
public class EffectDestory : MonoBehaviour
{
    public float destoryTime;
    private ParticleSystem[] ps;

    void Awake()
    {
        ps = GetComponentsInChildren<ParticleSystem>();
    }

    private void OnEnable()
    {
        CancelInvoke();
        Invoke("DestoryEffect",destoryTime);
        for (int i = 0; i < ps.Length; i++)
        {
            ps[i].Play();
        }
    }

    private void DestoryEffect()
    {
        gameObject.SetActive(false);
    }
}
