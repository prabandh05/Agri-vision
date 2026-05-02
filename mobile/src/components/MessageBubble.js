import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Animated, TouchableOpacity } from 'react-native';
import { Colors, Fonts, Spacing, Radius, CategoryMeta } from '../constants/theme';

/**
 * MessageBubble — renders a single chat message (user or AI).
 * Supports markdown-like bold (**text**) and bullet (•) rendering.
 */
export default function MessageBubble({ message }) {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(16)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 1, duration: 300, useNativeDriver: true }),
      Animated.spring(slideAnim, { toValue: 0, friction: 8, useNativeDriver: true }),
    ]).start();
  }, []);

  const isUser = message.role === 'user';
  const isTyping = message.type === 'typing';

  return (
    <Animated.View
      style={[
        styles.wrapper,
        isUser ? styles.wrapperUser : styles.wrapperAI,
        { opacity: fadeAnim, transform: [{ translateY: slideAnim }] },
      ]}
    >
      {!isUser && (
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>🌱</Text>
        </View>
      )}

      <View style={[styles.bubble, isUser ? styles.bubbleUser : styles.bubbleAI]}>
        {isTyping ? (
          <TypingIndicator />
        ) : (
          <>
            {message.title && !isUser && (
              <Text style={styles.bubbleTitle}>{message.title}</Text>
            )}
            <FormattedText text={message.text} isUser={isUser} />
            {message.followUps?.length > 0 && !isUser && (
              <FollowUpChips followUps={message.followUps} onPress={message.onFollowUp} />
            )}
          </>
        )}
      </View>

      {isUser && (
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>👤</Text>
        </View>
      )}
    </Animated.View>
  );
}

// ─── Formatted Text (mini markdown) ─────────────────────────────────────────

function FormattedText({ text, isUser }) {
  if (!text) return null;

  const lines = text.split('\n');
  const textColor = isUser ? Colors.userText : Colors.aiText;

  return (
    <View>
      {lines.map((line, idx) => {
        if (!line.trim()) return <View key={idx} style={{ height: 4 }} />;

        // Parse bold (**text**)
        const parts = line.split(/\*\*(.*?)\*\*/g);

        return (
          <Text key={idx} style={[styles.bubbleText, { color: textColor }]}>
            {parts.map((part, i) =>
              i % 2 === 1
                ? <Text key={i} style={styles.boldText}>{part}</Text>
                : part
            )}
          </Text>
        );
      })}
    </View>
  );
}

// ─── Follow-up Chips ──────────────────────────────────────────────────────────

function FollowUpChips({ followUps, onPress }) {
  if (!followUps?.length || !onPress) return null;
  return (
    <View style={styles.followUpsContainer}>
      <Text style={styles.followUpsLabel}>💬 Ask more:</Text>
      {followUps.slice(0, 3).map((q, i) => (
        <TouchableOpacity key={i} style={styles.followUpChip} onPress={() => onPress(q)} activeOpacity={0.7}>
          <Text style={styles.followUpText}>{q}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

// ─── Typing Indicator ─────────────────────────────────────────────────────────

function TypingIndicator() {
  const dot1 = useRef(new Animated.Value(0)).current;
  const dot2 = useRef(new Animated.Value(0)).current;
  const dot3 = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const animate = (dot, delay) =>
      Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(dot, { toValue: -6, duration: 300, useNativeDriver: true }),
          Animated.timing(dot, { toValue: 0, duration: 300, useNativeDriver: true }),
          Animated.delay(600),
        ])
      ).start();

    animate(dot1, 0);
    animate(dot2, 200);
    animate(dot3, 400);
  }, []);

  return (
    <View style={styles.typingRow}>
      {[dot1, dot2, dot3].map((dot, i) => (
        <Animated.View
          key={i}
          style={[styles.dot, { transform: [{ translateY: dot }] }]}
        />
      ))}
    </View>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  wrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    marginVertical: Spacing.xs,
    marginHorizontal: Spacing.md,
  },
  wrapperUser: { justifyContent: 'flex-end' },
  wrapperAI:   { justifyContent: 'flex-start' },

  avatar: {
    width: 32, height: 32,
    borderRadius: 16,
    backgroundColor: Colors.surfaceHigh,
    alignItems: 'center', justifyContent: 'center',
    marginHorizontal: Spacing.xs,
  },
  avatarText: { fontSize: 16 },

  bubble: {
    maxWidth: '75%',
    paddingVertical: Spacing.sm + 2,
    paddingHorizontal: Spacing.md,
    borderRadius: Radius.lg,
  },
  bubbleUser: {
    backgroundColor: Colors.userBubble,
    borderBottomRightRadius: 4,
  },
  bubbleAI: {
    backgroundColor: Colors.aiBubble,
    borderBottomLeftRadius: 4,
    borderWidth: 1,
    borderColor: Colors.surfaceBorder,
  },

  bubbleTitle: {
    fontSize: Fonts.sizes.sm,
    fontWeight: Fonts.weights.bold,
    color: Colors.primary,
    marginBottom: Spacing.xs,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  bubbleText: {
    fontSize: Fonts.sizes.md,
    lineHeight: 22,
    color: Colors.aiText,
  },
  boldText: {
    fontWeight: Fonts.weights.bold,
    color: Colors.primaryLight,
  },

  followUpsContainer: {
    marginTop: Spacing.sm,
    borderTopWidth: 1,
    borderTopColor: Colors.surfaceBorder,
    paddingTop: Spacing.sm,
  },
  followUpsLabel: {
    fontSize: Fonts.sizes.xs,
    color: Colors.textMuted,
    marginBottom: Spacing.xs,
  },
  followUpChip: {
    backgroundColor: Colors.primaryGlow,
    borderWidth: 1,
    borderColor: Colors.primaryDark,
    borderRadius: Radius.full,
    paddingVertical: 4,
    paddingHorizontal: Spacing.sm,
    marginVertical: 2,
    alignSelf: 'flex-start',
  },
  followUpText: {
    fontSize: Fonts.sizes.xs,
    color: Colors.primaryLight,
  },

  typingRow: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingVertical: 4 },
  dot: {
    width: 8, height: 8,
    borderRadius: 4,
    backgroundColor: Colors.primary,
  },
});
