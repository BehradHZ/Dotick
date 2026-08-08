import { useCallback, useEffect, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';

// Must be prefixed with EXPO_PUBLIC_ to be readable here — see
// .env.example for how to set this per-machine (LAN IP for phone access).
const API_URL = process.env.EXPO_PUBLIC_API_URL;
const HEALTH_ENDPOINT = `${API_URL}/api/health/`;

// 'idle' | 'loading' | 'success' | 'error'
function useHealthCheck() {
  const [status, setStatus] = useState('idle');
  const [detail, setDetail] = useState(null);

  const check = useCallback(async () => {
    if (!API_URL) {
      setStatus('error');
      setDetail(
        'EXPO_PUBLIC_API_URL is not set. Copy .env.example to .env and fill it in.'
      );
      return;
    }

    setStatus('loading');
    setDetail(null);

    try {
      const response = await fetch(HEALTH_ENDPOINT);
      const body = await response.json().catch(() => null);

      if (!response.ok || !body || body.status !== 'ok') {
        setStatus('error');
        setDetail(`Backend responded with HTTP ${response.status}.`);
        return;
      }

      setStatus('success');
      setDetail(body);
    } catch (err) {
      setStatus('error');
      // A generic "Failed to fetch" / TypeError here (rather than an
      // HTTP error status handled above) almost always means the
      // request never reached the app's response-handling code at
      // all — most commonly because:
      //   1. The backend isn't running, or API_URL points at the
      //      wrong host/port (e.g. localhost from a phone, which
      //      resolves to the phone itself, not the laptop).
      //   2. The browser blocked it as cross-origin (CORS). This is
      //      invisible here and in Django's logs — check the
      //      browser's own devtools console/network tab for a CORS
      //      error, and confirm the backend's DJANGO_CORS_ALLOWED_ORIGINS
      //      includes this app's exact origin (see backend/.env.example).
      const message = err instanceof Error ? err.message : String(err);
      setDetail(
        `${message} — backend unreachable at ${HEALTH_ENDPOINT}. If the ` +
          `backend is running, this is usually a CORS or wrong-host issue ` +
          `(check the browser console/network tab, and see backend/.env.example).`
      );
    }
  }, []);

  useEffect(() => {
    check();
  }, [check]);

  return { status, detail, retry: check };
}

export default function App() {
  const { status, detail, retry } = useHealthCheck();

  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>Dotick</Text>
        <Text style={styles.subtitle}>Stage 1 — Basic Foundation</Text>

        <View style={styles.card}>
          <Text style={styles.cardLabel}>Backend connection</Text>
          <Text style={styles.endpoint}>{HEALTH_ENDPOINT}</Text>

          {status === 'loading' && (
            <View style={styles.row}>
              <ActivityIndicator />
              <Text style={styles.statusText}>Checking…</Text>
            </View>
          )}

          {status === 'success' && (
            <View>
              <Text style={[styles.statusText, styles.statusOk]}>
                ✓ Connected — browser → Django → PostgreSQL → response
              </Text>
              <Text style={styles.responseText}>
                {JSON.stringify(detail)}
              </Text>
            </View>
          )}

          {status === 'error' && (
            <View>
              <Text style={[styles.statusText, styles.statusError]}>
                ✗ Could not confirm the connection
              </Text>
              <Text style={styles.responseText}>{String(detail)}</Text>
            </View>
          )}

          <Pressable style={styles.button} onPress={retry}>
            <Text style={styles.buttonText}>Retry</Text>
          </Pressable>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f7',
  },
  scrollContent: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
    color: '#1c1c1e',
  },
  subtitle: {
    fontSize: 14,
    color: '#6e6e73',
    marginTop: 4,
    marginBottom: 32,
  },
  card: {
    width: '100%',
    maxWidth: 420,
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 4 },
    elevation: 2,
  },
  cardLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#6e6e73',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  endpoint: {
    fontSize: 13,
    color: '#8a8a8e',
    marginTop: 4,
    marginBottom: 16,
    fontFamily: 'monospace',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  statusText: {
    fontSize: 15,
    fontWeight: '500',
    marginTop: 4,
  },
  statusOk: {
    color: '#1a7f37',
  },
  statusError: {
    color: '#c0362c',
  },
  responseText: {
    fontSize: 13,
    color: '#4b4b4f',
    marginTop: 8,
    fontFamily: 'monospace',
  },
  button: {
    marginTop: 20,
    backgroundColor: '#1c1c1e',
    borderRadius: 8,
    paddingVertical: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#ffffff',
    fontWeight: '600',
    fontSize: 14,
  },
});