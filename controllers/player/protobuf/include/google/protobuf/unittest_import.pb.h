// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: google/protobuf/unittest_import.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_google_2fprotobuf_2funittest_5fimport_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_google_2fprotobuf_2funittest_5fimport_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3017000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3017003 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
#include "google/protobuf/unittest_import_public.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_google_2fprotobuf_2funittest_5fimport_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_google_2fprotobuf_2funittest_5fimport_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxiliaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_google_2fprotobuf_2funittest_5fimport_2eproto;
namespace protobuf_unittest_import {
class ImportMessage;
struct ImportMessageDefaultTypeInternal;
extern ImportMessageDefaultTypeInternal _ImportMessage_default_instance_;
}  // namespace protobuf_unittest_import
PROTOBUF_NAMESPACE_OPEN
template<> ::protobuf_unittest_import::ImportMessage* Arena::CreateMaybeMessage<::protobuf_unittest_import::ImportMessage>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace protobuf_unittest_import {

enum ImportEnum : int {
  IMPORT_FOO = 7,
  IMPORT_BAR = 8,
  IMPORT_BAZ = 9
};
bool ImportEnum_IsValid(int value);
constexpr ImportEnum ImportEnum_MIN = IMPORT_FOO;
constexpr ImportEnum ImportEnum_MAX = IMPORT_BAZ;
constexpr int ImportEnum_ARRAYSIZE = ImportEnum_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* ImportEnum_descriptor();
template<typename T>
inline const std::string& ImportEnum_Name(T enum_t_value) {
  static_assert(::std::is_same<T, ImportEnum>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function ImportEnum_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    ImportEnum_descriptor(), enum_t_value);
}
inline bool ImportEnum_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, ImportEnum* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<ImportEnum>(
    ImportEnum_descriptor(), name, value);
}
enum ImportEnumForMap : int {
  UNKNOWN = 0,
  FOO = 1,
  BAR = 2
};
bool ImportEnumForMap_IsValid(int value);
constexpr ImportEnumForMap ImportEnumForMap_MIN = UNKNOWN;
constexpr ImportEnumForMap ImportEnumForMap_MAX = BAR;
constexpr int ImportEnumForMap_ARRAYSIZE = ImportEnumForMap_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* ImportEnumForMap_descriptor();
template<typename T>
inline const std::string& ImportEnumForMap_Name(T enum_t_value) {
  static_assert(::std::is_same<T, ImportEnumForMap>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function ImportEnumForMap_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    ImportEnumForMap_descriptor(), enum_t_value);
}
inline bool ImportEnumForMap_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, ImportEnumForMap* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<ImportEnumForMap>(
    ImportEnumForMap_descriptor(), name, value);
}
// ===================================================================

class ImportMessage final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:protobuf_unittest_import.ImportMessage) */ {
 public:
  inline ImportMessage() : ImportMessage(nullptr) {}
  ~ImportMessage() override;
  explicit constexpr ImportMessage(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  ImportMessage(const ImportMessage& from);
  ImportMessage(ImportMessage&& from) noexcept
    : ImportMessage() {
    *this = ::std::move(from);
  }

  inline ImportMessage& operator=(const ImportMessage& from) {
    CopyFrom(from);
    return *this;
  }
  inline ImportMessage& operator=(ImportMessage&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline const ::PROTOBUF_NAMESPACE_ID::UnknownFieldSet& unknown_fields() const {
    return _internal_metadata_.unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(::PROTOBUF_NAMESPACE_ID::UnknownFieldSet::default_instance);
  }
  inline ::PROTOBUF_NAMESPACE_ID::UnknownFieldSet* mutable_unknown_fields() {
    return _internal_metadata_.mutable_unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const ImportMessage& default_instance() {
    return *internal_default_instance();
  }
  static inline const ImportMessage* internal_default_instance() {
    return reinterpret_cast<const ImportMessage*>(
               &_ImportMessage_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(ImportMessage& a, ImportMessage& b) {
    a.Swap(&b);
  }
  inline void Swap(ImportMessage* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(ImportMessage* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline ImportMessage* New() const final {
    return new ImportMessage();
  }

  ImportMessage* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<ImportMessage>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const ImportMessage& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom(const ImportMessage& from);
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message* to, const ::PROTOBUF_NAMESPACE_ID::Message& from);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  ::PROTOBUF_NAMESPACE_ID::uint8* _InternalSerialize(
      ::PROTOBUF_NAMESPACE_ID::uint8* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(ImportMessage* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "protobuf_unittest_import.ImportMessage";
  }
  protected:
  explicit ImportMessage(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kDFieldNumber = 1,
  };
  // optional int32 d = 1;
  bool has_d() const;
  private:
  bool _internal_has_d() const;
  public:
  void clear_d();
  ::PROTOBUF_NAMESPACE_ID::int32 d() const;
  void set_d(::PROTOBUF_NAMESPACE_ID::int32 value);
  private:
  ::PROTOBUF_NAMESPACE_ID::int32 _internal_d() const;
  void _internal_set_d(::PROTOBUF_NAMESPACE_ID::int32 value);
  public:

  // @@protoc_insertion_point(class_scope:protobuf_unittest_import.ImportMessage)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::internal::HasBits<1> _has_bits_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  ::PROTOBUF_NAMESPACE_ID::int32 d_;
  friend struct ::TableStruct_google_2fprotobuf_2funittest_5fimport_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// ImportMessage

// optional int32 d = 1;
inline bool ImportMessage::_internal_has_d() const {
  bool value = (_has_bits_[0] & 0x00000001u) != 0;
  return value;
}
inline bool ImportMessage::has_d() const {
  return _internal_has_d();
}
inline void ImportMessage::clear_d() {
  d_ = 0;
  _has_bits_[0] &= ~0x00000001u;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 ImportMessage::_internal_d() const {
  return d_;
}
inline ::PROTOBUF_NAMESPACE_ID::int32 ImportMessage::d() const {
  // @@protoc_insertion_point(field_get:protobuf_unittest_import.ImportMessage.d)
  return _internal_d();
}
inline void ImportMessage::_internal_set_d(::PROTOBUF_NAMESPACE_ID::int32 value) {
  _has_bits_[0] |= 0x00000001u;
  d_ = value;
}
inline void ImportMessage::set_d(::PROTOBUF_NAMESPACE_ID::int32 value) {
  _internal_set_d(value);
  // @@protoc_insertion_point(field_set:protobuf_unittest_import.ImportMessage.d)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace protobuf_unittest_import

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::protobuf_unittest_import::ImportEnum> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::protobuf_unittest_import::ImportEnum>() {
  return ::protobuf_unittest_import::ImportEnum_descriptor();
}
template <> struct is_proto_enum< ::protobuf_unittest_import::ImportEnumForMap> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::protobuf_unittest_import::ImportEnumForMap>() {
  return ::protobuf_unittest_import::ImportEnumForMap_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_google_2fprotobuf_2funittest_5fimport_2eproto
