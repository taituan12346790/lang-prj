2.1 Quy trình tương tác và xử lý của hệ thống AI Agent
Hệ thống được triển khai dưới dạng một ứng dụng web tương tác, trong đó người học đóng vai trò trung tâm và AI Agent đóng vai trò là một người hướng dẫn thông minh có khả năng hỗ trợ học tập thông qua việc điều phối các thành phần xử lý khác nhau. Quy trình sử dụng bắt đầu từ lớp xác thực người dùng, bao gồm đăng nhập hoặc đăng ký tài khoản, sau đó người học lựa chọn ngôn ngữ muốn học và trình độ khởi đầu phù hợp. Trong trường hợp người dùng muốn bắt đầu ở mức cao hơn A1, hệ thống sẽ yêu cầu thực hiện bài kiểm tra đầu vào nhằm xác định mức độ kiến thức hiện tại trước khi cho phép vào giao diện học chính.
Sau khi người dùng truy cập vào hệ thống, mọi yêu cầu học tập đều đi qua luồng xử lý trung tâm theo cơ chế chat tương tác. Trước khi thực hiện các bước suy luận hoặc gọi công cụ, hệ thống áp dụng lớp kiểm tra đầu vào (Input Guardrail) để phát hiện các nội dung nhạy cảm, bao gồm ngôn từ chửi bậy, nội dung tình dục, chính trị, tôn giáo hoặc các chủ đề không phù hợp với phạm vi hỗ trợ học tập. Nếu đầu vào vi phạm chính sách, hệ thống sẽ từ chối phản hồi theo cách an toàn và dừng toàn bộ luồng xử lý tiếp theo.
Nếu đầu vào hợp lệ, hệ thống sẽ truy xuất bộ nhớ người dùng để lấy lịch sử hội thoại, tiến trình học tập, trình độ hiện tại và các tín hiệu học tập đã được tích lũy trước đó. Dựa trên thông tin đầu vào và trạng thái hiện tại, hệ thống sử dụng cơ chế lập kế hoạch chiến lược (strategy planning) kết hợp với phân loại ý định (intent detection) để xác định cách xử lý phù hợp cho từng yêu cầu. Thay vì phụ thuộc hoàn toàn vào khả năng suy luận của mô hình ngôn ngữ, các luồng xử lý chính (learning strategies) được thiết kế sẵn nhằm đảm bảo tính nhất quán, cá nhân hóa và định hướng sư phạm trong quá trình học tập.
Trong giai đoạn thực thi, hệ thống kích hoạt các công cụ (Tools) chuyên biệt tương ứng với từng loại yêu cầu. Cụ thể, Grammar Checker được sử dụng để phân tích và phát hiện lỗi ngữ pháp, Translation Tool hỗ trợ dịch thuật, trong khi Exercise Generator tạo bài tập luyện tập dựa trên lỗi sai của người học. Đối với các yêu cầu cần bổ sung kiến thức hoặc giải thích khái niệm, hệ thống áp dụng cơ chế Retrieval-Augmented Generation (RAG) để truy xuất thông tin liên quan từ cơ sở dữ liệu vector thông qua thành phần Retriever, nhằm cung cấp ngữ cảnh chính xác cho quá trình sinh phản hồi. Trong trường hợp không cần dùng tool, hệ thống sẽ chuyển trực tiếp sang mô hình ngôn ngữ để sinh câu trả lời theo đúng mục tiêu học tập đã được xác định.
Mô hình ngôn ngữ lớn (LLM) chủ yếu đảm nhiệm vai trò xử lý ngôn ngữ tự nhiên, bao gồm diễn đạt lại kết quả, cung cấp giải thích và hỗ trợ tạo nội dung học tập ở dạng dễ hiểu. Việc phân tách rõ vai trò giữa backend logic và mô hình ngôn ngữ giúp hệ thống duy trì tính ổn định và giảm thiểu các sai lệch không mong muốn trong quá trình phản hồi. Trước khi phản hồi được gửi đến người dùng, kết quả được đưa qua lớp kiểm định (Validator) nhằm đánh giá mức độ phù hợp về nội dung, tính nhất quán với dữ liệu truy xuất và tuân thủ các nguyên tắc sư phạm đã được thiết kế. Trong trường hợp kết quả chưa đạt yêu cầu, hệ thống có thể thực hiện điều chỉnh hoặc tái xử lý nhằm cải thiện chất lượng đầu ra.
Cuối cùng, phản hồi được gửi đến người dùng thông qua giao diện chat, đồng thời hệ thống cập nhật lại bộ nhớ bao gồm lịch sử hội thoại, lỗi sai và tiến trình học tập của người học. Bên cạnh đó, hệ thống còn theo dõi các chỉ số kỹ thuật (xác định thông qua tần suất dùng đúng ngữ pháp, cấu trúc, từ vựng; các lỗi sai dần được làm đúng; trả lời đúng liên tục các dạng bài khó, không phát sinh ra chỗ hổng kiến thức) để đánh giá khả năng tiến bộ của từng người dùng theo thời gian. Khi hệ thống nhận thấy người học đã đạt đủ tín hiệu tiến bộ để nâng trình độ, hệ thống sẽ đề xuất làm bài kiểm tra lên level; nếu người dùng vượt qua bài test, hệ thống sẽ cập nhật trực tiếp trình độ mới vào profile. Điều này giúp đảm bảo khả năng tích lũy tri thức dài hạn, hỗ trợ cá nhân hóa và tạo ra một lộ trình học tập phù hợp hơn cho từng người dùng.












2.2 Tổng quan chương trình
Để hiện thực hóa hệ thống AI Agent hỗ trợ học ngoại ngữ với khả năng phản hồi chính xác, cá nhân hóa cao và đảm bảo bảo mật dữ liệu, toàn bộ hệ thống được thiết kế theo kiến trúc web hiện đại, dễ mở rộng và có khả năng vận hành ổn định trong thực tế. Hệ thống được xây dựng với backend FastAPI để xử lý các API một cách nhanh chóng và bất đồng bộ, frontend Streamlit để tạo giao diện chat tương tác trực quan, đồng thời kết hợp LangChain và LangGraph để quản lý luồng xử lý có trạng thái, lập kế hoạch và điều phối công cụ một cách linh hoạt. Bên cạnh đó, FAISS được sử dụng làm vector database để lưu trữ và truy xuất embedding nhanh chóng, còn PostgreSQL được dùng làm user database để quản lý thông tin người dùng, lịch sử học tập và tiến trình cá nhân hóa.
Hệ thống AI Agent bao gồm hai thành phần cốt lõi chính:
2.2.1 Mô hình điều phối và tương tác chính (Main Agent Model)
Hệ thống sử dụng mô hình GPT-OSS 120B thông qua API cloud của Groq làm mô hình điều phối trung tâm. Với cấu trúc lớn và khả năng xử lý ngôn ngữ tự nhiên mạnh, GPT-OSS 120B đảm nhiệm vai trò là LLM Agent chính, chịu trách nhiệm tiếp nhận đầu vào từ giao diện chat, phối hợp với bộ nhớ người dùng, lập kế hoạch xử lý và sinh phản hồi phù hợp theo ngữ cảnh học tập. Việc sử dụng mô hình cloud giúp hệ thống tận dụng được năng lực suy luận mạnh hơn của LLM, đồng thời vẫn đảm bảo tốc độ phản hồi gần thời gian thực nhờ hạ tầng xử lý tối ưu từ Groq.
2.2.2 Mô hình nhúng và truy xuất tri thức (Embedding & Retrieval)
Để hỗ trợ truy xuất tri thức chính xác, hệ thống sử dụng mô hình BGE-M3 làm mô hình nhúng. Nhờ cơ chế hybrid retrieval kết hợp Dense, Sparse và Multi-vector, BGE-M3 cho phép hệ thống thực hiện Retrieval-Augmented Generation (RAG) hiệu quả trên cơ sở dữ liệu vector FAISS. Điều này giúp AI Agent truy xuất nhanh chóng và chính xác các tài liệu liên quan về ngữ pháp, từ vựng và mẫu câu thực tế, từ đó nâng cao độ tin cậy và tính sư phạm của phản hồi.


1. PROJECT ROOT (phiên bản “build được”, không over-engineer, tuy nhiên chưa áp dụng được cho PostgreSQL, chưa có chức năng đăng nhập/đăng ký, làm các bái test)
project_root/
lang_prj/
├── .env
├── config.py
├── docker_compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes_chat.py
│   │
│   ├── core/
│   │   ├── database.py
│   │   ├── intent_classifier.py
│   │   ├── language_parser.py
│   │   ├── pipeline.py
│   │   ├── planner.py
│   │   ├── reflector.py
│   │   ├── register_tools.py
│   │   ├── router.py
│   │   ├── strategy.py
│   │   └── validator.py
│   │
│   ├── llm/
│   │   ├── llm_client.py
│   │   └── prompts.py
│   │
│   ├── memory/
│   │   ├── long_term.py
│   │   ├── memory_service.py
│   │   └── short_term.py
│   │
│   ├── models/
│   │   ├── exercise_result.py
│   │   ├── learning_session.py
│   │   ├── memory_entry.py
│   │   ├── user.py
│   │   └── user_profile.py
│   │
│   ├── rag/
│   │   ├── base_retriever.py
│   │   ├── df_retriever_lite.py
│   │   ├── embeddings.py
│   │   ├── graph_store.py
│   │   ├── ingest.py
│   │   ├── init_retriever.py
│   │   ├── test_retrieval.py
│   │   └── vector_store.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── profile.py
│   │   └── test.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── test.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── learning_service.py
│   │   ├── level_service.py
│   │   └── test_service.py
│   │
│   ├── tools/
│   │   ├── exercise_generator.py
│   │   ├── exercise_generator_wrapper.py
│   │   ├── grammar_checker.py
│   │   ├── grammar_checker_wrapper.py
│   │   ├── tool_registry.py
│   │   └── translator.py
│   │   └── translator_wrapper.py
│   │
│   └── utils/
│       ├── helpers.py
│       ├── level_utils.py
│       └── security.py
├── data/
│   ├── raw/                    # tài liệu học
│   └── processed/  




