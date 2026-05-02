import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../engine/query_engine.dart';
import 'browse_screen.dart';

class Message {
  final String text;
  final bool isUser;
  final String? title;

  Message({required this.text, required this.isUser, this.title});
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Message> _messages = [
    Message(
      text: "Namaskara! 🙏 I'm your offline agricultural advisor for Mandya.\n\nAsk me about crops, diseases, or government schemes.",
      isUser: false,
    )
  ];
  final QueryEngine _queryEngine = QueryEngine();
  bool _isLoading = false;

  void _handleSend() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add(Message(text: text, isUser: true));
      _controller.clear();
      _isLoading = true;
    });

    final result = await _queryEngine.processQuery(text);

    setState(() {
      _messages.add(Message(
        text: result.answer,
        isUser: false,
        title: result.title,
      ));
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("AgriVision"),
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.grid_view_rounded, color: Color(0xFF4CAF6F)),
          onPressed: () async {
            final result = await Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const BrowseScreen()),
            );
            if (result != null && result is String) {
              _controller.text = result;
              _handleSend();
            }
          },
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () {},
          )
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return _ChatBubble(message: msg);
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),
          _InputBar(
            controller: _controller,
            onSend: _handleSend,
          ),
        ],
      ),
    );
  }
}

class _ChatBubble extends StatelessWidget {
  final Message message;

  const _ChatBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 8),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: message.isUser
              ? const Color(0xFF1B5E20)
              : const Color(0xFF1E3022),
          borderRadius: BorderRadius.circular(16).copyWith(
            bottomRight: message.isUser ? const Radius.circular(0) : null,
            bottomLeft: !message.isUser ? const Radius.circular(0) : null,
          ),
          border: Border.all(
            color: const Color(0xFF2A4030),
            width: 1,
          ),
        ),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.8,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (message.title != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Text(
                  message.title!,
                  style: const TextStyle(
                    color: Color(0xFF4CAF6F),
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                    letterSpacing: 1.1,
                  ),
                ),
              ),
            MarkdownBody(
              data: message.text,
              styleSheet: MarkdownStyleSheet(
                p: TextStyle(
                  color: message.isUser ? const Color(0xFFC8E6C9) : const Color(0xFFE8F5E9),
                  fontSize: 15,
                  height: 1.4,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _InputBar extends StatelessWidget {
  final TextEditingController controller;
  final VoidCallback onSend;

  const _InputBar({required this.controller, required this.onSend});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: const BoxDecoration(
        color: Color(0xFF152217),
        border: Border(top: BorderSide(color: Color(0xFF2A4030))),
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: controller,
              decoration: InputDecoration(
                hintText: "Ask about crops...",
                hintStyle: const TextStyle(color: Color(0xFF5C8A62)),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                  borderSide: BorderSide.none,
                ),
                fillColor: const Color(0xFF0D1B0F),
                filled: true,
                contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              ),
            ),
          ),
          const SizedBox(width: 8),
          CircleAvatar(
            backgroundColor: const Color(0xFF4CAF6F),
            child: IconButton(
              icon: const Icon(Icons.send, color: Color(0xFF0D1B0F)),
              onPressed: onSend,
            ),
          ),
        ],
      ),
    );
  }
}
