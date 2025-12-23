"use client";

import { useEffect, useState } from 'react';

export interface NotificationSettings {
  enabled: boolean;
  autoRunAlerts: boolean;
  vetoAlerts: boolean;
  soundEnabled: boolean;
}

export function useNotifications() {
  const [permission, setPermission] = useState<NotificationPermission>(() =>
    typeof window !== 'undefined' && 'Notification' in window
      ? Notification.permission
      : 'default'
  );
  const [settings, setSettings] = useState<NotificationSettings>(() => {
    if (typeof window === 'undefined') {
      return {
        enabled: false,
        autoRunAlerts: true,
        vetoAlerts: true,
        soundEnabled: true,
      };
    }

    // localStorage에서 설정 불러오기
    const savedSettings = localStorage.getItem('afo-notification-settings');
    if (savedSettings) {
      try {
        return JSON.parse(savedSettings);
      } catch (e) {
        console.warn('알림 설정 파싱 실패:', e);
      }
    }

    return {
      enabled: false,
      autoRunAlerts: true,
      vetoAlerts: true,
      soundEnabled: true,
    };
  });

  // 권한 상태 변경 모니터링
  useEffect(() => {
    if ('Notification' in window) {
      const handlePermissionChange = () => {
        setPermission(Notification.permission);
      };

      // 권한 변경 이벤트 리스너 (일부 브라우저에서 지원)
      if ('permissions' in navigator) {
        navigator.permissions.query({ name: 'notifications' }).then((result) => {
          result.addEventListener('change', handlePermissionChange);
        });
      }

      return () => {
        // cleanup if needed
      };
    }
  }, []);

  // 권한 요청
  const requestPermission = async () => {
    if (!('Notification' in window)) {
      alert('이 브라우저는 알림을 지원하지 않습니다.');
      return false;
    }

    try {
      const result = await Notification.requestPermission();
      setPermission(result);
      return result === 'granted';
    } catch (error) {
      console.error('알림 권한 요청 실패:', error);
      return false;
    }
  };

  // 설정 저장
  const updateSettings = (newSettings: Partial<NotificationSettings>) => {
    const updated = { ...settings, ...newSettings };
    setSettings(updated);
    localStorage.setItem('afo-notification-settings', JSON.stringify(updated));
  };

  // 알림 전송
  const sendNotification = (title: string, body: string, data?: any) => {
    if (permission !== 'granted' || !settings.enabled) {
      return;
    }

    try {
      const notification = new Notification(title, {
        body,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        tag: data?.trace_id ? `verdict-${data.trace_id}` : 'afo-notification',
        data,
        requireInteraction: false,
        silent: !settings.soundEnabled,
      });

      // 클릭 이벤트 처리
      notification.onclick = () => {
        window.focus();
        notification.close();
      };

      // 자동 닫힘 (5초 후)
      setTimeout(() => {
        notification.close();
      }, 5000);

    } catch (error) {
      console.error('알림 전송 실패:', error);
    }
  };

  // verdict 이벤트에 따른 알림
  const notifyVerdict = (verdict: any) => {
    if (!verdict) return;

    const { decision, trinity_score, veto_triggered, rule_id } = verdict;

    if (decision === 'AUTO_RUN' && settings.autoRunAlerts) {
      sendNotification(
        '🚀 AUTO_RUN 승인',
        `Trinity Score ${trinity_score}/100 - 자동 실행됩니다`,
        verdict
      );
    } else if (veto_triggered && settings.vetoAlerts) {
      sendNotification(
        '🚫 VETO 발동',
        `헌법 개정안 0001에 따라 Commander 승인이 필요합니다`,
        verdict
      );
    } else if (decision === 'ASK' && settings.vetoAlerts) {
      sendNotification(
        '⏳ 수동 검토 필요',
        `Trinity Score ${trinity_score}/100 - 형님의 승인이 필요합니다`,
        verdict
      );
    }
  };

  return {
    permission,
    settings,
    requestPermission,
    updateSettings,
    sendNotification,
    notifyVerdict,
    isSupported: 'Notification' in window,
  };
}
