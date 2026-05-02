import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  FlatList, StyleSheet, KeyboardAvoidingView, Platform,
  ActivityIndicator, StatusBar,
} from 'react-native';
import { Colors, Fonts, Spacing, Radius, Shadow } from '../constants/theme';
import MessageBubble from '../components/MessageBubble';
import SuggestionChips from '../components/SuggestionChips';
import { processQuery } from '../engine/QueryEngine';
import { initDatabase } from '../database/DatabaseService';

const WELCOME_MESSAGE = {
  id: 'welcome',
  role: 'assistant',
  title: 'AgriVision — Your Farming Advisor',
  text: `**Namaskara! 🙏**\n\nI'm your offline agricultural advisor for Mandya district.\n\nI can help you with:\n• 🔴 Crop diseases & pest management\n• 🧪 Fertilizer schedules & dosage\n• 💧 Irrigation & water management\n• 🌾 Crop recommendations by season\n• 🏛️ Government schemes & subsidies\n• 🌿 Organic farming methods\n\nAsk me anything in English or describe your farm problem!`,
  followUps: [
    'My paddy leaves have brown spots',
    'What crops for Kharif season?',
    'How to get PM-KISAN benefits?',
  ],
};

export default function ChatScreen({ route }) {
  const [messages, setMessages]   = useState([WELCOME_MESSAGE]);
  const [input, setInput]         = useState('');
  const [loading, setLoading]     = useState(false);
  const [dbReady, setDbReady]     = useState(false);
  const [showChips, setShowChips] = useState(true);
  const flatListRef = useRef(null);
  let msgIdCounter  = useRef(100);

  // Init DB on mount
  useEffect(() => {
    initDatabase()
      .then(() => setDbReady(true))
      .catch(err => {
        console.error('DB init failed:', err);
        addMessage('assistant', '⚠️ Database failed to load. Please restart the app.', null, []);
      });
  }, []);

  // Handle initial query from navigation
  useEffect(() => {
    if (route?.params?.initialQuery && dbReady) {
      handleSend(route.params.initialQuery);
    }
  }, [dbReady, route?.params?.initialQuery]);

  const addMessage = useCallback((role, text, title, followUps) => {
    const id = String(++msgIdCounter.current);
    setMessages(prev => [...prev, { id, role, text, title, followUps }]);
    setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100);
  }, []);

  const handleSend = useCallback(async (queryText) => {
    const q = (queryText || input).trim();
    if (!q || !dbReady) return;

    setInput('');
    setShowChips(false);

    // Add user message
    const userId = String(++msgIdCounter.current);
    setMessages(prev => [...prev, { id: userId, role: 'user', text: q }]);

    // Add typing indicator
    const typingId = 'typing';
    setMessages(prev => [...prev, { id: typingId, role: 'assistant', type: 'typing', text: '' }]);
    setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100);

    setLoading(true);
    try {
      const response = await processQuery(q);

      // Remove typing indicator, add real response
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== typingId);
        const newId = String(++msgIdCounter.current);
        return [...filtered, {
          id: newId,
          role: 'assistant',
          text: response.answer,
          title: response.title,
          followUps: response.followUps || [],
          onFollowUp: (fq) => handleSend(fq),
        }];
      });
    } catch (err) {
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== typingId);
        return [...filtered, {
          id: String(++msgIdCounter.current),
          role: 'assistant',
          text: '⚠️ Something went wrong. Please try again.',
          followUps: [],
        }];
      });
    } finally {
      setLoading(false);
      setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 200);
    }
  }, [input, dbReady]);

  const renderItem = useCallback(({ item }) => (
    <MessageBubble
      message={{
        ...item,
        onFollowUp: item.onFollowUp || ((q) => handleSend(q)),
      }}
    />
  ), [handleSend]);

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <StatusBar barStyle="light-content" backgroundColor={Colors.background} />

      {/* DB Loading Banner */}
      {!dbReady && (
        <View style={styles.loadingBanner}>
          <ActivityIndicator color={Colors.primary} size="small" />
          <Text style={styles.loadingText}>  Loading agricultural database...</Text>
        </View>
      )}

      {/* Message List */}
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: false })}
      />

      {/* Suggestion Chips */}
      {showChips && (
        <SuggestionChips onPress={handleSend} />
      )}

      {/* Input Bar */}
      <View style={styles.inputBar}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Ask about your crops, diseases, schemes..."
          placeholderTextColor={Colors.textMuted}
          multiline
          maxLength={500}
          onFocus={() => setShowChips(false)}
          returnKeyType="send"
          blurOnSubmit={false}
          onSubmitEditing={() => handleSend()}
        />
        <TouchableOpacity
          style={[styles.sendBtn, (!input.trim() || loading) && styles.sendBtnDisabled]}
          onPress={() => handleSend()}
          disabled={!input.trim() || loading}
          activeOpacity={0.8}
        >
          {loading
            ? <ActivityIndicator color={Colors.textDark} size="small" />
            : <Text style={styles.sendIcon}>➤</Text>
          }
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container:    { flex: 1, backgroundColor: Colors.background },
  loadingBanner:{
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: Spacing.sm,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.surfaceBorder,
  },
  loadingText:  { color: Colors.textSecondary, fontSize: Fonts.sizes.sm },
  listContent:  { paddingTop: Spacing.md, paddingBottom: Spacing.sm },

  inputBar: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    backgroundColor: Colors.surface,
    borderTopWidth: 1,
    borderTopColor: Colors.surfaceBorder,
    gap: Spacing.sm,
  },
  input: {
    flex: 1,
    backgroundColor: Colors.background,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
    borderRadius: Radius.lg,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.sm,
    color: Colors.textPrimary,
    fontSize: Fonts.sizes.md,
    maxHeight: 120,
  },
  sendBtn: {
    width: 44, height: 44,
    borderRadius: 22,
    backgroundColor: Colors.primary,
    alignItems: 'center', justifyContent: 'center',
    ...Shadow.glow,
  },
  sendBtnDisabled: { backgroundColor: Colors.surfaceHigh, shadowOpacity: 0 },
  sendIcon:        { fontSize: 18, color: Colors.textDark, fontWeight: 'bold' },
});
